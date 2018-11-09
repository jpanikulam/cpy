"""Abstract code containers.

    TODO:
        - Handle templates in a real way
"""
from collections import OrderedDict
import formatting


class CpyVar(object):
    def __init__(self, cpp_type, name, default=None, sympy_symbol=None, qualifiers=[], is_ref=False):
        self.cpp_type = cpp_type
        self.name = name
        self.default = default
        self.sympy_symbol = sympy_symbol
        self.qualifiers = qualifiers
        self.is_ref = is_ref

    def declaration(self):
        line_lcontents = [self.cpp_type]
        line_lcontents.extend(self.qualifiers)
        line_lcontents.append('{ref}{name}'.format(
            ref='&' if self.is_ref else '',
            name=self.name
        ))
        return ' '.join(line_lcontents)

    def declare(self):
        """
        TODO:
            Do something smart if this is a reference
        """
        line_lcontents = [self.cpp_type]
        line_lcontents.extend(self.qualifiers)
        line_lcontents.append(self.name)

        line_rcontents = []
        if self.default is not None:
            line_rcontents.append(self.default)

        return formatting.form_line(line_lcontents, line_rcontents)


class CpyScope(object):
    def __init__(self, name='cpy_generated', enclosing_scope=None, end_in_semicolon=False):
        self.name = name
        self.enclosing_scope = enclosing_scope
        self.end_in_semicolon = end_in_semicolon
        self.code = ''

        self.started = False
        self.ended = False

    def declaration(self):
        return 'namespace {}'.format(self.name)

    def line(self, *args, **kwargs):
        self.code += formatting.form_line(*args, **kwargs)

    def write(self, text):
        self.code += text

    def start(self):
        enter_text = ''
        enter_text += self.declaration()
        enter_text += '{'
        self.write(enter_text)

    def end(self):
        exit_text = ''
        exit_text += '}'
        if self.end_in_semicolon:
            exit_text += ';'

        self.write(exit_text)

        if self.enclosing_scope:
            self.enclosing_scope.write(self.code)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.end()

    def __str__(self):
        return self.code


class CpyCode(CpyScope):
    def __init__(self, name, headers=[], header=True):
        super(CpyCode, self).__init__(name=name)
        if header:
            self.write('#pragma once\n')

        for header in headers:
            self.add_header(header)

    def add_header(self, header):
        self.write('#include <{header}>\n'.format(header=header))


class CpyIf(CpyScope):
    def __init__(self, condition, enclosing_scope):
        super(CpyIf, self).__init__(name="If", enclosing_scope=enclosing_scope, end_in_semicolon=False)
        self.condition = condition

    def declaration(self):
        return "if ({})".format(self.condition)


class CpyClass(CpyScope):
    def __init__(self, name, enclosing_scope, base_class=None):
        super(CpyClass, self).__init__(name=name, enclosing_scope=enclosing_scope, end_in_semicolon=True)
        assert isinstance(base_class, (str, type(None))), 'CPY does not yet support inherting from CPY classes'
        self.base_class = base_class

    def declaration(self):
        if self.base_class is not None:
            return 'class {name} : public {base}'.format(name=self.name, base=str(self.base_class))
        else:
            return 'class {name}'.format(name=self.name)

    def public(self):
        self.write('public: \n')


class CpyFunction(CpyScope):
    def __init__(self, return_type, name, enclosing_scope=None, args=[], qualifiers=[]):
        super(CpyFunction, self).__init__(enclosing_scope=enclosing_scope)

        self.name = name

        # TODO: Use CPY types
        assert isinstance(return_type, str), "For now, the return type must be a string."
        self.return_type = return_type

        for arg in args:
            # TODO: Let people do whatever they want
            assert isinstance(arg, CpyVar), "Arguments must be CpyVars"

        self.args = args
        self.enclosing_scope = enclosing_scope
        self.qualifiers = qualifiers

    @property
    def _arg_string(self):
        declarations = map(lambda arg: arg.declaration(), self.args)
        return ', '.join(declarations)

    def declaration(self):
        return ' '.join([self.return_type, self.name, '(', self._arg_string, ')', ' '.join(self.qualifiers)])

    def __str__(self):
        return '{name}: ({inputs}) -> {return_type}'.format(
            name=self.name,
            return_type=self.return_type,
            inputs=self.args
        )


def to_type(cpp_type):
    assert isinstance(cpp_type, str)
    return cpp_type


class CpyStruct(CpyScope):
    def __init__(self, name, enclosing_scope=None):
        super(CpyStruct, self).__init__(enclosing_scope=enclosing_scope, end_in_semicolon=True)
        self.members = []
        self.name = name

    def add_member(self, cpp_type, name):
        self.members.append(((to_type(cpp_type)), name))

    def generate(self):
        """Generate code for this class.

        It is generally expected that one will not call this until done.

        TODO:
            - Everything should use this method instead of line-by-lining
        """
        self.start()
        for member in self.members:
            # self.write(member.declare())
            self.line(*member)
        self.end()

    def declaration(self):
        return 'struct ' + self.name

    def __str__(self):
        return self.name + ': ' + str(self.members)

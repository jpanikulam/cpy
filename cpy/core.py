"""Tools for syntactic code generation.

Why:
    - It is not always the case that an AST is the easiest
        representation of a code
    - It is often easier to think in terms of syntax than it is to think in terms of
        graph structures
    - This tool is intended to be used for scientific code generation, and not really
        for production tools

How:
    - Python is the future
    - Code is generated in *sequence*

Design:
    - Functions & scopes should be defined abstractly, and can be arbitrarily inserted
      into the Code singleton

:: With
    - With statements for writing into scopes
        - Everything is done in sequence
        - It's hard to track what is being written
        - It's hard to get what exists (And then do something with that)
        - It's hard to track dependencies

:: No With
    - Code generation is less syntactic
    - You have to manually end scopes, which is unclean

Imagined end-game (Success Criteria for Phase 1)
    - Generate an EKF that abuses arbitrary sparsity
        - Stretch-goal: Use SSE
            - https://felix.abecassis.me/2011/09/cpp-getting-started-with-sse/
            - https://software.intel.com/sites/default/files/a6/22/18072-347603.pdf
    - Generate Boost::Python bindings for structs defined in Python

"""
from collections import OrderedDict
import sympy
import formatting


class Code(object):
    """Code object.

    Intended to be used as a singleton for managing a codebase
    """
    def __init__(self, author=None, desc=None):
        self.abstract_elements = {}
        self.code_text = "// This code was generated using CPY: a tool by Jacob Panikulam"
        if author:
            self.code_text += "// Author: {}\n".format(author)
        if desc:
            self.code_text += "// {}\n".format(desc)
        self.code_text += "\n"

        # If you're having trouble following so far, this is not an AST
        self.syntax_dict = {
            'functions': [],
            'structs': [],
            'globals': []
        }

        self.stale = True

    def comment(self, text):
        self.code_text += '//' + text + '\n'

    def line(self, *args):
        text = ' '.join(args)
        text += ';'
        self.code_text += text

    def write(self, arg):
        self.code_text += arg

    def declare(self, cpp_type, name, default=None):
        defaults = {
            'int': 0,
            'double': 0.0,
            'float': 0.0,
        }

        if default is not None:
            self.line(cpp_type, name, '=', default)
        elif cpp_type in defaults:
            self.line(cpp_type, name, '=', str(defaults[cpp_type]))
        else:
            self.line(cpp_type, name)

    def fold(self, other):
        assert isinstance(other, Code), "Can only fold in another Code object"
        self.write(other.text)

    def add_function(self, cfunc):
        self.syntax_dict['functions'].append(cfunc)
        self.stale = True

    def add_struct(self, cstruct):
        self.syntax_dict['structs'].append(cstruct)
        self.stale = True

    def generate(self):
        # for function in self.syntax_dict['functions']:
        #     with GenFunc(function.name, self) as gen_func:
        #         for var in function.scope_vars:
        #             self.declare(**var)

        # for cstruct in self.syntax_dict['structs']:
        #     with GenStruct(self, cstruct.name) as gen_struct:
        #         for member_name, member_dict in cstruct.members.items():
        #             gen_struct.write_member(member_name, member_dict)

        text = ""
        for thing in self.children:
            text += thing.generate()
        self.stale = False

    @property
    def text(self):
        return self.code_text

    def __str__(self):
        if self.stale:
            self.generate()
        return formatting.clang_fmt(self.code_text)

    def __iadd__(self, arg):
        # Not clear to me why this doesn't work
        self.code_text += arg
        return self


class CppScope(Code):
    # def __init__(self, title_text):
    #     self.title_text = title_text
    #     self.children = []

    def insert(self, other):
        self.children.append(other)

    def generate(self):
        text = "{\n"
        for child in self.children:
            child.generate()
        text += "\n}"

"""    def __enter__(self, *args):
        self.code.write(self.title_text + '{')
        return self

    def __exit__(self, *args):
        self.code.write('}')
"""


class GenStruct(CppScope):
    def __init__(self, name, constructor=True):
        self.name = name
        self.title_text = 'struct {name}'.format(name=name)
        self.make_constructor = constructor
        self.members = OrderedDict()

    def write_member(self, name, member_dict):
        self.declare(
            member_dict['var_type'],
            name,
            member_dict['var_value'],
        )

    def add_member(self, name, member):
        self.members[name] = member

    def generate(self):
        text = "{\n"
        for member, contents in self.members.items():
            self.write_member(member, contents)
        text += "\n};"
        return text


# TODO
class GenFunc(CppScope):
    def __init__(self, code, name, return_type, *args):
        raise NotImplementedError
        self.name = name
        self.code = code
        self.args = args
        self.title_text = '{return_type} {name} ({args})'.format(
            name=self.name,
            return_type=return_type,
            args=self.arsg
        )
        self.members = {}

    def write_member(self, name, member_dict):
        self.code.declare(
            member_dict['var_type'],
            name,
            member_dict['var_value'],
        )

    def __exit__(self, *args):
        self.code.write('};')


def main():
    pass


if __name__ == '__main__':
    main()

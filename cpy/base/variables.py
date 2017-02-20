from cpy.base import types
from cpy.base import language
from cpy.base import str_helpers

class Variable(object):
    def __init__(self, cpp_type, name, qualifiers=[], ref=False, value=None):
        self._type = cpp_type
        self._name = name

        # If qualifiers was not a list, make it into a list
        if not len(qualifiers):
            qualifiers = [qualifiers]

        for qualfier in qualifiers:
            language.validate_qualifier(qualfier)

        self.qualifiers = qualifiers

        self._ref = ref
        self.value = value

    def declare(self):
        return "{qualifiers}{type} {ref}{name}".format(
            qualifiers=' '.join(self.qualifiers) + ' ' if self.qualifiers else '',
            type=self.type.name,
            ref='&' if self.ref else '',
            name=self._name
        )

    def set_declare(self, text):
        declaration = self.declare()
        return "{decl} = {text}".format(decl=declaration, text=text)

    def declare_default(self):
        return self.set_declare(self.value)

    @property
    def ref(self):
        return self._ref

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def const(self):
        return 'const' in self.qualifiers

    @property
    def constexpr(self):
        return 'constexpr' in self.qualifiers

    @property
    def volatile(self):
        return 'volatile' in self.qualifiers

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.declare()


def to_variable(text):
    """TODO: Use clang."""
    new_text, _ = str_helpers.get_remove(text, ';')

    qualifiers = []
    for qualifier in language.qualifiers:
        new_text, present = str_helpers.get_remove(new_text, qualifier)

        if present:
            qualifiers.append(qualifier)

    if ' = ' in new_text:
        new_text, value = new_text.split(' = ')

    else:
        # TODO: Allow constructor
        value = None


    if ('<' in text) and ('>' in text):
        template = str_helpers.between(new_text, '<', '>')
        new_text = str_helpers.not_between(new_text, '<', '>')

        template_arguments = str_helpers.clean_split(template, ',')
    else:
        template_arguments = []


    type_name, var_text = new_text.split(' ')
    # Name
    var_name, ref = str_helpers.get_remove(var_text, '&')

    # Type manipulation
    var_type = types.Type(type_name, template_arguments=template_arguments)

    return Variable(var_type, var_name, qualifiers=qualifiers, value=value, ref=ref)


if __name__ == '__main__':

    xtz = "const Eigen::Vector<double, 1, 2> &silly = Eigen::Vector(0.0, 1.0, 2.0);"
    xtz_var = to_variable(xtz)
    print xtz_var.type.template_arguments
    print xtz_var.declare_default()
    print xtz_var.ref

    print '\\' * 20
    t = types.Type('Eigen::Vector', ['double', '1', '2'])
    var = Variable(t, 'silly', ['const'], ref=True)
    print var.declare()
    print t
    print var
    print repr(var)

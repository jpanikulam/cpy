from cpy2 import CpyVar
import cpy2


class CpyBindings(cpy2.CpyScope):
    def __init__(self, name, enclosing_scope):
        super(CpyBindings, self).__init__(enclosing_scope=enclosing_scope)
        self.members = []
        self.name = name

    def declaration(self):
        module_name = "BOOST_PYTHON_MODULE({struct_name}_py)".format(struct_name=self.name)
        return module_name

    # Really, though:
    # cpy abstracts should accumulate state and then produce some output
    def add_class(self, cpy_class):
        self.write('boost::python::class_<{struct_name}>("{struct_name}", boost::python::init<>())'.format(
            struct_name=self.name)
        )
        for member in cpy_class.members:
            self.write('.def_readwrite("{name}", &{struct_name}::{name})'.format(
                name=member.name,
                struct_name=self.name)
            )
        self.write(';')


def make_bindings(struct_name, variables):
    pass


def make_bound_struct(struct_name, variables):
    headers = [
        "boost/python.hpp"
    ]

    code = cpy2.CpyCode(name='auglag', headers=headers, header=False)
    code.start()

    # with cpy2.CpyStruct(name=struct_name, enclosing_scope=code) as base_class:
    base_class = cpy2.CpyStruct(name=struct_name, enclosing_scope=code)
    for var in variables:
        base_class.add_member(var)
    base_class.generate()

    with CpyBindings(name=struct_name, enclosing_scope=code) as binding_class:
        # for var in variables:
            # binding_class.write("boost::python::class_<{struct_name}>".format(struct_name=struct_name))
        binding_class.add_class(base_class)

    code.end()
    print(cpy2.clang_fmt(code))
    return code


if __name__ == '__main__':

    _vars = [
        CpyVar('double', 'v_0', 0.0),
        CpyVar('double', 'v_1', 2.0),
        CpyVar('double', 'v_2'),
    ]
    code = make_bound_struct('missile', _vars)
    from cpy2 import compile
    compile.easy_build(code)

Implementation Guide
====================

This document outlines the implementation of CPY2. These are developer details.


# What should a user have to do?

1. Define header/file boundaries (Or shove it all in a single file)
    a. The user (unfortunately) will have to specify explicit includes (i.e. interfacing with human-written C++)
2. In each scope, define the variables that will be used and their types
3. In each scope, write C++ lines
    a. If possible, write CPY expressions that will be formed into code
        This should look like `code.write(expression)`
    b. CPY expressions should be handled, whenever possible, as very thin wrappers around Sympy symbols
4.

# What should a user NOT have to do?

* Figure out which headers need to be included, and where
* Write their own benchmarks for crazy code

# What should a user be able to do?

* Generate ultra-fast C++ code for doing matrix multiplication
* Specify contracts so that unittests can be auto-generated
    * Some of those contracts can just be input validity contracts
    * Others can be more complicated
* Programmatically produce lots of C++ using very little Python
    * (Notion: C++ has a very low entropy density, while Python has the opposite)


# Details
* soft-asserts: Accumulate errors that let the *generating* code keep running, but make the *generated* code invalid. Then shout about these errors at the completion of generation or the first error.
* super-soft-asserts: Accumulate things that might be errors in the generated code, but we have no way to know


# Example Code
```
with Function(name='cobombole', code=code):
    x = {sympy matrix expression}
    code.write(x)

    # soft-asserts non-void
    code.return_val(x)

# Lazily generate the code, then return the code string, print
print code
```

```
my_struct = CStruct(name='ModelParamters')

my_struct.add_members(
    # Soft assert valid type...?
    CVar('double', 'mass', qualifiers='const'),
    CVar('double', 'I_z', qualifiers='const'),
    CVar('double', 'I_y', qualifiers='const'),
)

# Declare at the beginning of the current scope and then write it
code.add(my_struct)
```


```

```

```
if ... {type} containts eigen:
    EIGEN_MAKE_ALIGNED_OPERATOR_NEW
```

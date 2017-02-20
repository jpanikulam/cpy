"""CPY is a Python syntactic code generation toolbox.

It aim to provide tools to developers, covering a few basic needs:

    - Producing C++ code that can be used in production C++ products
    - High performance matrix math, that takes advantage of sparsity
        (And when it can't, defaults to letting Eigen do the work)
    - High performance math that takes advantage of SSE4, NTStore, and other processor-specific features in a way that compilers often can't
    - Easy tools for writing code from Python
        - Easy tools for generating python bindings for that code
        - And easy tools for generating unittests for that code


CPY aims to make the task of programatically writing C++ **easy**. Everything else is secondary.
"""
import setuptools

description = "The Python syntactic code generation tool"

setuptools.setup(
    name='cpy',
    version='1.0',
    license='MIT',
    long_description=__doc__,
    url='jakepanikul.am',
    author_email='jpanikul@gmail.com',
    packages=setuptools.find_packages(),
    description=description,
    keywords="code generation codegen numerics SSE AVX C++ cpp",
    platforms='any',
    zip_safe=True
)

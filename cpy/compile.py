"""Compiler Playground

Experimentally compile CPY scripts

What on Earth is this?
    - Generate a CMakeLists file (What!?)
    - Build and link everything (WHAT!?)
    - Did my generate code compile?

TODO:
    1. Create a CMake file from CPY targets
        - (Make it easy to do this without rigorously defining targets)
    2. Create a tempdir and write all of the code there
    3. Run cmake, then make
    4. Provide the user with the errors

"""
import tempfile
import os
import shutil

from logging import Log
import compilers
import formatting
import cmake


def temp_build_dir(lib_name, build_path=None):
    if build_path is None:
        Log.warn("Building in tmp directory")
        folder = tempfile.mkdtemp(prefix='cpy-')
    else:
        Log.info("Building at {}".format(build_path))
        assert os.path.exists(build_path), "Build path must exist!"
        folder = build_path

    targ = cmake.Target(
        lib_name, ['test.cc'],
        {
            'Boost': '1.45.0',
            'PythonLibs': '2.7',
            'Eigen3': None
        },
        executable=False
    )

    cmake_file = cmake.CMake('.', python=True)
    cmake_file.add_target(targ)
    formatting.put_file(folder, 'CMakeLists.txt', cmake_file.text)

    build_folder = os.path.join(folder, 'build')
    os.mkdir(build_folder)
    return folder


def easy_build(code, clean_up=True, build_path=None):
    path = temp_build_dir('my_test_lib', build_path)
    formatting.put_file(path, 'test.cc', code, True)

    Log.br()
    Log.note("Cmaking...")
    build_folder = os.path.join(path, 'build')
    cmake_output = cmake.cmake(path, build_folder)
    Log.note('CMake Output:')
    Log.br()
    print(cmake_output)
    Log.br()

    Log.note("Building...")
    make_output, success = cmake.make(build_folder)
    Log.br()
    if success:
        Log.note("Success! Make Output:")
    else:
        Log.error("ERROR: Make failed, output:")
    compilers.gcc.prettify_output(make_output)

    Log.br()

    # Clean up the build folder, now that the output has been generated
    if clean_up:
        Log.warn('Cleaning up build output...')
        shutil.rmtree(path)


if __name__ == '__main__':
    code = """
#include <boost/python.hpp>
namespace auglag {
struct missile {
  double v_0 = 0.0;
  double v_1 = 2.0;
  double v_2;
};
BOOST_PYTHON_MODULE(missile_py) {
  boost::python::class_<missile>("missile", boost::python::init<>())
      .def_readwrite("v_0", &missile::v_0)
      .def_readwrite("v_1", &missile::v_1)
      .def_readwrite("v_2", &missile::v_2);
}
}"""
    easy_build(code, clean_up=True)

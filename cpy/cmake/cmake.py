"""Generating CMake files.

TODO:
    - Directory structure
    - Release types
    - Funkier stuff

"""
import os
import subprocess

from cpy.logging import Log


_known_include_vars = {
    'Boost': '${Boost_INCLUDE_DIR}',
    'PythonLibs': '${PYTHON_INCLUDE_DIRS}',
    'catkin': "${catkin_INCLUDE_DIRS}",
    'Eigen3': "${EIGEN3_INCLUDE_DIR}",
}

_known_lib_vars = {
    'Boost': '${Boost_LIBRARIES}',
    'PythonLibs': '${PYTHON_LIBRARIES}',
    'catkin': '',
    'Eigen3': '',
}


class Target(object):
    def __init__(self, name, sources, libraries={}, executable=True):
        self.name = name
        self.sources = sources
        self.libraries = libraries
        self.executable = executable

    def add_library(self, library):
        self.libraries.update(library)

    def bind_python(self, module_name):
        """Create Boost Python bindings."""
        pass


class CMake(object):
    def __init__(self, base_path, python=False):

        self._base_path = os.path.realpath(base_path)
        self.linked_libs = set()

        self.text = ""
        self.cmd("CMAKE_MINIMUM_REQUIRED", "VERSION 2.8")

        self.title_comment("Configure CMake")
        # Set up build type
        self.set("CMAKE_BUILD_TYPE", "DEBUG")

        # Set up module path
        self.set(
            "CMAKE_MODULE_PATH",
            "${PROJECT_SOURCE_DIR}/cmake"
        )

        # Get those nice angle brackets working
        self.set(
            "BASEPATH",
            '"${CMAKE_CURRENT_SOURCE_DIR}"'
        )
        self.include_dirs('"${BASEPATH}"')

        flags = [
            '-std=c++11',
            '-fPIC',
            '-Wall',
            '-Wextra',
            '-Wno-unused-parameter',
            '-Wno-unused-variable',
        ]
        self.set(
            'CMAKE_CXX_FLAGS',
            '"${CMAKE_CXX_FLAGS} ' +
            ' '.join(flags) + '"'
        )

        boost_configs = [
            "Boost_USE_STATIC_LIBS OFF",
            "Boost_USE_MULTITHREADED ON",
            "Boost_USE_STATIC_RUNTIME OFF",
        ]

        if python:
            self.title_comment("Configure Boost")
            map(self.set, boost_configs)
            self.linked_libs.add("Boost")
            self.cmd("find_package", "Boost", "1.45.0")
            self.cmd("find_package", "Boost", "COMPONENTS", "python", "REQUIRED")
            self.include_dirs("${Boost_INCLUDE_DIR}")

    def title_comment(self, text):
        self.write('\n' + '#' * 40)
        self.write('# {}'.format(text))
        self.write('#' * 40 + '\n')

    def cmd(self, cmd_name, *args):
        """TODO: Support kwargs."""
        if len(args) > 2:
            self.write('{cmd}(\n\t{args}\n)'.format(cmd=cmd_name.upper(), args='\n\t'.join(args)))
        else:
            self.write('{cmd}({args})'.format(cmd=cmd_name.upper(), args=' '.join(args)))

    def set(self, *args):
        # self.write('SET(' + ' '.join(args) + ')')
        self.cmd('set', *args)

    def include_dirs(self, include_dir):
        assert isinstance(include_dir, str), "Include include_dir must be a string!"
        self.cmd('include_directories', include_dir)

    def add_library(self, target):
        # self.write("ADD_LIBRARY(" + target.name + ' ' + ' '.join(target.sources) + ')')
        self.cmd('add_library', target.name, *target.sources)

    def swap_dict(self, _list, _dict):
        new_list = []
        for element in _list:
            if element in _dict.keys():
                new_list.append(_dict[element])
            else:
                new_list.append(element)
        return new_list

    def link_libraries(self, target):
        for library_name, version in target.libraries.items():
            if library_name not in self.linked_libs:
                self.linked_libs.add(library_name)

                if version is None:
                    version = ""

                self.write("FIND_PACKAGE({} {} REQUIRED)".format(library_name, version))

                if library_name in _known_include_vars.keys():
                    self.include_dirs(_known_include_vars[library_name])

        # adjusted_includes = self.swap_dict(target.libraries, _known_include_vars)
        adjusted_libraries = self.swap_dict(target.libraries, _known_lib_vars)
        self.cmd("TARGET_LINK_LIBRARIES", target.name, *adjusted_libraries)
        self.cmd(
            "SET_TARGET_PROPERTIES",
            target.name,
            'PROPERTIES PREFIX ""',
            'LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/bindings"'
        )

    def add_target(self, target):
        self.title_comment("Build {}".format(target.name))
        if target.executable:
            raise NotImplementedError("Uh oh, we don't support this yet")
        else:
            self.add_library(target)
            self.link_libraries(target)

    def write(self, text):
        self.text += text + '\n'


def cmake(source_folder, build_folder):
    """Call the `cmake` command

    :param source_folder: The path to the code (Where the CMakeLists.txt file lives)
    :param build_folder: The path to the folder where the cmake output should be

    TODO:
        - return success
    """
    assert os.path.exists(source_folder), "Build folder must exist!"
    assert os.path.exists(build_folder), "Source folder must exist!"
    assert "CMakeLists.txt" in os.listdir(source_folder), "Must be a file called CMakeLists.txt in the source folder!"

    cmake_args = "cmake -B{build} -H{source}".format(source=source_folder, build=build_folder)
    Log.info('$ ' + cmake_args)
    cmake_out = subprocess.check_output(cmake_args, shell=True)
    return cmake_out


def make(build_folder):
    assert os.path.exists(build_folder), "Build path does not exist {}".format(build_folder)
    make_args = "make -C {build}".format(build=build_folder)
    Log.info('$ ' + make_args)
    try:
        make_out = subprocess.check_output(make_args, stderr=subprocess.STDOUT, shell=True)
        return make_out, True

    except(subprocess.CalledProcessError) as exc:
        return exc.output, False


if __name__ == '__main__':
    targ = Target(
        'MissileBindings', ['test.cc'],
        {
            'Boost': '1.45.0',
            'PythonLibs': '2.7',
            'Eigen3': None
        },
        executable=False
    )

    cm = CMake('.', python=True)
    cm.add_target(targ)

    print(cm.text)

"""Parse yaml files and turn them into builders"""

import os
import sys
import yaml
from string import Template

import settings
from builder import Builder
from utils import safe_mkdir, sys_command
from template import load_templated_yaml_rep
from component import load_all_packages

def yaml_builders_in_path(path):
    """Return list of all yaml builders in the given path. Look through
    directory for files with .yaml extension"""

    yaml_ext = '.yaml'

    # Files as basename, ext tuples
    all_files = [os.path.splitext(f) for f in os.listdir(path)]

    return [basename for basename, ext in all_files if ext == yaml_ext]

def builder_by_name_yaml(name, load_dependencies=True):
    """Given a name, return a yaml builder of that name, or None if it is
    unavailable"""

    # yaml_dir = settings.yaml_dir
    # yaml_ext = '.yaml'

    # name = name.lower()

    # if name in yaml_builders_in_path(yaml_dir):
    #     filename = os.path.join(yaml_dir, name + yaml_ext)
    #     return builder_from_yaml(filename, load_dependencies)

    yaml_rep = load_templated_yaml_rep(name)

    return builder_from_yaml(yaml_rep, load_dependencies)

def handle_dependencies(yamlBuilder, yaml_rep):
    """Scan yaml_rep for dependencies. If they exist, check whether they are
    installed. If not, attempt to install. Once installed, add the relevant
    directories to necessary environment variables, in particular:

    * Add bin to PATH
    * Add include to CPATH
    * Add lib to LIBRARY_PATH
    * Add lib to LD_LIBRARY_PATH
    * Add pkgconfig to PKG_CONFIG_PATH

    After updating paths, set CPPFLAGS and LDFLAGS appropriately. This will
    overwrite existing values.
    """

    for dependency in yaml_rep['dependencies']:
        builder_dep = builder_by_name_yaml(dependency)

        if builder_dep is None:
            raise Exception('Unknown dependency {}'.format(dependency))

        dep_installed = builder_dep.check_stage_finished("INSTALL")

        if not dep_installed:
            builder_dep.process_all_stages()

        yamlBuilder.env_manager.add_to_pathvar('CPATH', builder_dep.include_dir)
        yamlBuilder.env_manager.add_to_pathvar('LIBRARY_PATH', 
                                               builder_dep.lib_dir)
        yamlBuilder.env_manager.add_to_pathvar('LD_LIBRARY_PATH', 
                                               builder_dep.lib_dir)

        pkgconfig_dir = builder_dep.pkgconfig_dir
        if pkgconfig_dir:
            yamlBuilder.env_manager.add_to_pathvar('PKG_CONFIG_PATH', 
                                                   builder_dep.pkgconfig_dir)

        bin_dir = os.path.join(builder_dep.install_dir, 'bin')
        yamlBuilder.env_manager.add_path(bin_dir)

    yamlBuilder.env_manager.update_CPPFLAGS()
    yamlBuilder.env_manager.update_LDFLAGS()

def builder_from_yaml(yaml_rep, load_dependencies=True):

    url = yaml_rep['url']
    name = yaml_rep['name']
    version = yaml_rep['version']

    yamlBuilder = Builder(name, url)
    yamlBuilder._version = str(version)
    yamlBuilder.yaml_rep = yaml_rep

    #print yaml_rep

    var_list = { 'prefix' : yamlBuilder.install_dir,
                 'version' : yamlBuilder.version,
                 'libdir' : yamlBuilder.lib_dir,
                 'includedir' : yamlBuilder.include_dir,
                 'installdir' : yamlBuilder.install_dir,
                 'name' : yamlBuilder.name}

    # FIXME - ugly

    if 'dependencies' in yaml_rep:
        yamlBuilder.dependencies = yaml_rep['dependencies']
        if load_dependencies:
            handle_dependencies(yamlBuilder, yaml_rep)

    if 'use_build_dir' in yaml_rep:
        if yaml_rep['use_build_dir'] is True:
            yamlBuilder.build_in_source = False

    if 'build' in yaml_rep:
        def user_build(self):
            os.chdir(self.build_dir)
            for command in yaml_rep['build']:
                template_command = Template(command)
                try:
                    spaced_command = template_command.substitute(var_list).split(" ")
                except KeyError, e:
                    print "Error parsing yaml file, parameter ${}".format(e.args[0])
                    sys.exit(1)

                self.system(spaced_command)

        yamlBuilder.user_build = user_build

    if 'install' in yaml_rep:
        def user_install(self):
            os.chdir(self.build_dir)
            for command in yaml_rep['install']:
                install_command = Template(command)
                spaced_command = install_command.substitute(var_list).split(" ")
                self.system(spaced_command)

        yamlBuilder.user_install = user_install

    if 'configure_opts' in yaml_rep:
        yamlBuilder.configure_opts = yaml_rep['configure_opts']

    if 'configure' in yaml_rep:
        def user_configure(self):
            os.chdir(self.build_dir)
            for command in yaml_rep['configure']:
                configure_command = Template(command)
                spaced_command = configure_command.substitute(var_list).split(" ")
                self.system(spaced_command)

        yamlBuilder.user_configure = user_configure


    if 'allscript' in yaml_rep:
        def user_allscript(self):
            os.chdir(self.build_dir)
            command = Template(yaml_rep['allscript'])
            spaced_command = command.substitute(var_list).split(" ")
            self.system(spaced_command)

        yamlBuilder.user_allscript = user_allscript

    if 'python_package' in yaml_rep:
        package_name = yaml_rep['python_package']
        def subpackage(self):
            install_command = ['easy_install', package_name]
            self.system(install_command)

        yamlBuilder.subpackage = subpackage

    if 'perl_package' in yaml_rep:
        package_name = yaml_rep['perl_package']
        def subpackage(self):
            install_command = ['cpan', package_name]
            self.system(install_command)

        yamlBuilder.subpackage = subpackage

    if 'source_prefix' in yaml_rep:
        source_prefix = yaml_rep['source_prefix']
        yamlBuilder.source_prefix = source_prefix

    if 'post_install' in yaml_rep:
        def post_install(self):
            for command in yaml_rep['post_install']:
                command_template = Template(command)
                spaced_command = command_template.substitute(var_list).split(" ")
                self.env_manager.run_command(spaced_command)

        yamlBuilder.post_install = post_install

    # FIXME - handle CPPFLAGS better
    if 'CPPFLAGS' in yaml_rep:
        yamlBuilder.env_manager.extra_CPPFLAGS = yaml_rep['CPPFLAGS']

    return yamlBuilder

def main():
    #builder_from_yaml(sys.argv[1])
    #builder_from_yaml('yaml/perl.yaml')
    builder_by_name_yaml(sys.argv[1])

if __name__ == '__main__':
    main()

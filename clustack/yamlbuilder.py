"""Parse yaml files and turn them into builders"""

import os
import yaml
from string import Template

import settings
from builder import Builder
from utils import safe_mkdir, sys_command

def yaml_builders_in_path(path):
    """Return list of all yaml builders in the given path. Look through
    directory for files with .yaml extension"""

    yaml_ext = '.yaml'

    # Files as basename, ext tuples
    all_files = [os.path.splitext(f) for f in os.listdir(path)]

    return [basename for basename, ext in all_files if ext == yaml_ext]

def builder_by_name_yaml(name):
    """Given a name, return a yaml builder of that name, or None if it is
    unavailable"""

    yaml_dir = settings.yaml_dir
    yaml_ext = '.yaml'

    if name in yaml_builders_in_path(yaml_dir):
        filename = os.path.join(yaml_dir, name + yaml_ext)
        return builder_from_yaml(filename)

def builder_from_yaml(yaml_file):

    with open(yaml_file) as f:
        yaml_rep = yaml.load(f)

    url = yaml_rep['url']
    name = yaml_rep['name']
    version = yaml_rep['version']

    yamlBuilder = Builder(name, url)
    yamlBuilder._version = str(version)

    print yaml_rep

    var_list = { 'prefix' : yamlBuilder.install_dir,
                 'version' : yamlBuilder.version,
                 'name' : yamlBuilder.name}

    if 'build' in yaml_rep:
        def user_build(self):
            os.chdir(self.build_dir)

            for command in yaml_rep['build']:
                self.system(command)

        yamlBuilder.user_build = user_build

    if 'install' in yaml_rep:
        def user_install(self):
            os.chdir(self.build_dir)
            for command in yaml_rep['install']:
                install_command = Template(command)
                spaced_command = install_command.substitute(var_list).split(" ")
                self.system(spaced_command)

        yamlBuilder.user_install = user_install

    if 'configure' in yaml_rep:
        def user_configure(self):
            os.chdir(self.build_dir)
            for command in yaml_rep['configure']:
                configure_command = Template(command)
                spaced_command = configure_command.substitute(var_list).split(" ")
                self.system(spaced_command)

        yamlBuilder.user_configure = user_configure

    if 'dependencies' in yaml_rep:
        python_dep = builder_by_name_yaml('python')
        bin_dir = os.path.join(python_dep.install_dir, 'bin')
        yamlBuilder.env_manager.add_path(bin_dir)
        yamlBuilder.system(['which', 'python'])

    if 'allscript' in yaml_rep:
        def user_allscript(self):
            os.chdir(self.build_dir)
            command = Template(yaml_rep['allscript'])
            spaced_command = command.substitute(var_list).split(" ")
            self.system(spaced_command)

        yamlBuilder.user_allscript = user_allscript


    return yamlBuilder

def main():
    builder_from_yaml('yaml/setuptools.yaml')
    #builder_from_yaml('yaml/perl.yaml')

if __name__ == '__main__':
    main()

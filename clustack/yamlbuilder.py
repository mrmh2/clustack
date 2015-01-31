"""Parse yaml files and turn them into builders"""

import os
import yaml
from string import Template

from builder import Builder
from utils import safe_mkdir, sys_command

def builder_from_yaml(yaml_file):

    with open(yaml_file) as f:
        yaml_rep = yaml.load(f)

    url = yaml_rep['url']
    name = yaml_rep['name']
    version = yaml_rep['version']

    yamlBuilder = Builder(name, url)
    yamlBuilder._version = str(version)

    print yaml_rep

    # make_com
    # def user_build(self):
    #     self.system()

    var_list = {'prefix' : yamlBuilder.install_dir}

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






    return yamlBuilder

def main():
    builder_from_yaml('yaml/htslib.yaml')

if __name__ == '__main__':
    main()

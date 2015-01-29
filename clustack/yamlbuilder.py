"""Parse yaml files and turn them into builders"""

import yaml

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

    def constructed_build(self):
        safe_mkdir(self.own_shelf_dir)

        os.chdir(self.full_unpack_dir)

        for command in yaml_rep['build']:
            sys_command(command)

    yamlBuilder.build = constructed_build

    yamlBuilder.install()

def main():
    builder_from_yaml('yaml/htslib.yaml')

if __name__ == '__main__':
    main()
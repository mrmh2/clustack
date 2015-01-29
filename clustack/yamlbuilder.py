"""Parse yaml files and turn them into builders"""

import yaml

from builder import Builder

def builder_from_yaml(yaml_file):

    with open(yaml_file) as f:
        yaml_rep = yaml.load(f)

    url = yaml_rep['url']
    name = yaml_rep['name']
    version = yaml_rep['version']

    yamlBuilder = Builder(name, url)
    yamlBuilder._version = version

    yamlBuilder.install()

def main():
    builder_from_yaml('yaml/zlib.yaml')

if __name__ == '__main__':
    main()
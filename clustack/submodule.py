import os

from yamlbuilder import builder_by_name_yaml

def parse_pip_line(pip_line):

    try:
        name, bversion = pip_line.split()
        version = bversion[1:-1]
        return name, version
    except ValueError:
        return None

class PythonModule(object):

    def __init__(self):
        pyBuilder = builder_by_name_yaml('python')
        bin_dir = os.path.join(pyBuilder.install_dir, 'bin')
        pyBuilder.env_manager.add_path(bin_dir)       
        self.builder = pyBuilder

        self.check_installed()

    def check_installed(self):
        raw_list = self.builder.check_output(['pip', 'list'])
        package_lines = raw_list.split('\n')

        # Parse lines into name, version tuples
        parsed_lines = [parse_pip_line(line) for line in package_lines]

        # Remove any elements that failed to parse
        parsed_lines = [pl for pl in parsed_lines if pl is not None]

        self.installed_packages = dict(parsed_lines)

    def query_package(self, name):
        print self.installed_packages
        return self.installed_packages[name]

def main():
    pm = PythonModule()

    print pm.query_package('numpy')


if __name__ == '__main__':
    main()
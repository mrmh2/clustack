"""Functions for installing a new package."""

import sys

import settings
from envmanager import EnvManager
from shelf import Shelf
from yamlbuilder import builder_by_name_yaml

class BuildEnvironment(EnvManager):

    def __init__(self):
        EnvManager.__init__(self)
        

def install_package(package_name):
    """Given a package name, determine package dependencies, install if
    necessary and then install the package."""

    # Generate build environment

    build_env = BuildEnvironment()

    current_shelf = Shelf()

    gcc_dependencies = current_shelf.find_all_dependencies('gcc')

    missing_dependencies = set(gcc_dependencies) - set(current_shelf.installed_packages)

    if len(missing_dependencies):
        print 'Missing dependencies:'
        print '\n'.join(missing_dependencies)
        sys.exit(2)

    for package_name in (gcc_dependencies + ['gcc']):
        package = current_shelf.find_package(package_name)
        package.update_env_manager(build_env)

    yaml_builder = builder_by_name_yaml(package_name)
    yaml_builder.env_manager = build_env

    yaml_builder.process_all_stages()

def main():
    package_name = sys.argv[1]

    install_package(package_name)

if __name__ == '__main__':
    main()

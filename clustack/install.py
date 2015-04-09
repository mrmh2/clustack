"""Functions for installing a new package."""

import os
import sys

import yaml

import settings
from envmanager import EnvManager
from shelf import Shelf
from yamlbuilder import builder_by_name_yaml
from blueprint import load_blueprint_by_name


class BuildEnvironment(EnvManager):

    def __init__(self):
        EnvManager.__init__(self)
        

def install_package(package_name):
    """Given a package name, determine package dependencies, install if
    necessary and then install the package."""

    print 'Installing {0}'.format(package_name)

    # Generate build environment

    build_env = BuildEnvironment()

    current_shelf = Shelf()

    gcc_dependencies = current_shelf.find_all_dependencies('gcc')

    missing_dependencies = set(gcc_dependencies) - set(current_shelf.installed_packages)

    if len(missing_dependencies):
        print 'Missing dependencies:'
        print '\n'.join(missing_dependencies)
        sys.exit(2)

    for dep_package_name in (gcc_dependencies + ['gcc']):
        package = current_shelf.find_package(dep_package_name)
        package.update_env_manager(build_env)
    
    package_blueprint = load_blueprint_by_name(package_name)
    dependencies = package_blueprint.direct_dependencies
    missing_dependencies = set(dependencies) - set(current_shelf.installed_packages)

    for dependency in missing_dependencies:
        install_package(dependency)

    for dependency in dependencies:
        package = current_shelf.find_package(dependency)
        package.update_env_manager(build_env)

    yaml_builder = builder_by_name_yaml(package_name, load_dependencies=False)

    yaml_builder.env_manager = build_env
    yaml_builder.env_manager.update_CPPFLAGS()
    yaml_builder.env_manager.update_LDFLAGS()

    yaml_builder.process_all_stages()

    yaml_builder.yaml_rep['environment_flags'] = build_env.my_env

    yaml_rep = yaml.dump(yaml_builder.yaml_rep, default_flow_style=False)

    receipt_path = os.path.join(yaml_builder.shelf_dir, settings.receipt_file)

    with open(receipt_path, 'w') as f:
        f.write(yaml_rep)


def main():
    package_name = sys.argv[1]

    install_package(package_name)

if __name__ == '__main__':
    main()

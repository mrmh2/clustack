import os

from yamlbuilder import builder_by_name_yaml
from blueprint import load_blueprint_by_name
import settings

def load_component_by_name(name):
    return Package(name)

def list_packages():
    """List all installed packages."""

    shelf_dir = settings.shelf_dir

    package_list = os.listdir(shelf_dir)

    package_list.sort()

    return package_list

def load_all_packages():
    """Load all installed packages.
    TODO: Move to environment type object."""

    package_dict = {n : load_component_by_name(n)
                    for n in list_packages()}

    return package_dict

class Component(object):
    pass

class Package(Component):
    def __init__(self, name):
        self.name = name

        self.blueprint = load_blueprint_by_name(name)
        self.builder = builder_by_name_yaml(name, load_dependencies=False)

    @property
    def source_dir(self):
        return self.builder.source_dir
        
    @property
    def bin_dir(self):
        return self.builder.bin_dir

    @property
    def include_dir(self):
        return self.builder.include_dir

    @property
    def lib_dir(self):
        return self.builder.lib_dir

    def update_stack(self, stack):

        stack.env_manager.add_to_pathvar('PATH', self.bin_dir)
        stack.env_manager.add_to_pathvar('CPATH', self.include_dir)
        stack.env_manager.add_to_pathvar('LIBRARY_PATH', self.lib_dir)
        stack.env_manager.add_to_pathvar('LD_LIBRARY_PATH', self.lib_dir)

    @property
    def full_dependencies(self):
        return self.blueprint.full_dependencies

    @property
    def direct_dependencies(self):
        return self.blueprint.direct_dependencies

    @property
    def version(self):
        return self.blueprint.version

"""Components are the parts of a software stack. They can be full packages or
subpackages of other packages (such as python packages or perl modules)."""

import os
import yaml
# from yamlbuilder import builder_by_name_yaml
# from blueprint import load_blueprint_by_name
import settings

from utils import safe_mkdir

def package_from_path(path):
    """Load a package from a filesystem path. Infer the name and version of the
    package from the path."""

    partial_path, version = os.path.split(path)
    base_path, name = os.path.split(partial_path)

    p = Package(name, version, path)

    return p

def package_from_yaml(yaml_file):
    """Load a package from a yaml receipt file."""

    with open(yaml_file) as f:
        yaml_rep = yaml.load(f)

    name = yaml_rep['name']
    version = yaml_rep['version']

    base_path, receipt_file = os.path.split(yaml_file)

    p = Package(name, version, base_path)

    try:
        p.direct_dependencies = yaml_rep['dependencies']
    except KeyError:
        pass

    return p

class PackageLoader(object):
    pass

class FileSystemLoader(PackageLoader):
    """A loader to load packages from the file system."""

    def __init__(self, base_path=None):
        if base_path is None:
            base_path = settings.shelf_dir

        self.base_path = base_path

        safe_mkdir(base_path)

    def load(self, name, version):

        full_path = os.path.join(self.base_path, name, version)

        receipt_file = os.path.join(full_path, settings.receipt_file)
        if os.path.isfile(receipt_file):
            return package_from_yaml(receipt_file)
        else:
            return package_from_path(full_path)

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

    package_dict = dict((n, load_component_by_name(n))
                    for n in list_packages())

    return package_dict

class Component(object):
    pass

class Package(Component):
    """Class representing an installed package."""

    def __init__(self, name, version, base_path):
        self.name = name
        self.version = version
        self.base_path = base_path
        self.arch = 'x86_64'

        self.direct_dependencies = []
        

        # self.blueprint = load_blueprint_by_name(name)
        # self.builder = builder_by_name_yaml(name, load_dependencies=False)

    @property
    def source_dir(self):
        return os.path.join(self.base_path, 'source')
        
    @property
    def bin_dir(self):
        return os.path.join(self.base_path, self.arch, 'bin')

    @property
    def include_dir(self):
        return os.path.join(self.base_path, self.arch, 'include')

    @property
    def lib_dir(self):
        return os.path.join(self.base_path, self.arch, 'lib')

    def update_stack(self, stack):

        stack.env_manager.add_to_pathvar('PATH', self.bin_dir)
        stack.env_manager.add_to_pathvar('CPATH', self.include_dir)
        stack.env_manager.add_to_pathvar('LIBRARY_PATH', self.lib_dir)
        stack.env_manager.add_to_pathvar('LD_LIBRARY_PATH', self.lib_dir)

    # @property
    # def full_dependencies(self):
    #     return self.blueprint.full_dependencies

    # @property
    # def direct_dependencies(self):
    #     return self.blueprint.direct_dependencies

    def __repr__(self):
        return "Package<{0}-{1}>".format(self.name, self.version)

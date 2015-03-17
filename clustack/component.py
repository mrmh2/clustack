import os

# from yamlbuilder import builder_by_name_yaml
# from blueprint import load_blueprint_by_name
import settings

from utils import safe_mkdir

def package_from_path(path):
    """Load a package from a filesystem path. Infer the name and version of the
    package from the path."""

    partial_path, version = os.path.split(path)
    base_path, name = os.path.split(partial_path)

    p = Package(name, version)
    p.base_path = path

    return p

class PackageLoader(object):
    pass

class FileSystemLoader(PackageLoader):

    def __init__(self, base_path=None):
        if base_path is None:
            base_path = settings.shelf_dir

        self.base_path = base_path

        safe_mkdir(base_path)

    def load(self, name):

        partial_path = os.path.join(self.base_path, name)

        versions = os.listdir(partial_path)

        if len(versions) > 1:
            raise Exception('Cannot handle more than one version of package')

        version = versions[0]

        full_path = os.path.join(partial_path, version)

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

    package_dict = {n : load_component_by_name(n)
                    for n in list_packages()}

    return package_dict

class Component(object):
    pass

class Package(Component):
    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.arch = 'x86_64'

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

    @property
    def full_dependencies(self):
        return self.blueprint.full_dependencies

    @property
    def direct_dependencies(self):
        return self.blueprint.direct_dependencies

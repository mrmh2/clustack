import os
import yaml

import settings

def load_blueprint_yaml(filename):
    """Load a blueprint from the given YAML file."""

    with open(filename) as f:
        yaml_rep = yaml.load(f)

    name = yaml_rep['name']
    
    bp = BluePrint(name)

    bp.version = yaml_rep['version']

    if 'dependencies' in yaml_rep:
        bp.direct_dependencies = yaml_rep['dependencies']

    return bp

def load_blueprint(filename):
    """Load a blueprint from the given filename. Try to determine the type of
    blueprint from the file extension and dispatch to the relevant loader."""

    path, ext = os.path.splitext(filename)

    try:
        loader = LOADERS[ext]
    except KeyError:
        raise Exception("Don't know how to load blueprint: {}".format(filename))

    return loader(filename)

def ext_matches(name, ext_list):
    """Return True if file extension is in the supplied list."""

    base, ext = os.path.splitext(name)

    return ext in ext_list

def get_basename_and_full_path(name, path):
    """Given name and path, return name with no extension and full path."""

    basename = os.path.splitext(name)[0]
    full_path = os.path.join(path, name)

    return basename, full_path

def get_available_blueprints():
    """Generate list of all available blueprints, in the form of a dictionary of
    name : path pairs."""

    available = {}

    bp_exts = settings.blueprint_exts
    bp_path = settings.blueprint_path

    for path in bp_path:
        matching_files = [f for f in os.listdir(path) 
                          if ext_matches(f, bp_exts)]

        md = dict(get_basename_and_full_path(fn, path) for fn in matching_files)

        available.update(md)

    return available
    
def load_blueprint_by_name(name):
    """Load a blueprint from a (string) name. Use settings to determine search
    path, then choose a loader."""

    name = name.lower()

    available_blueprints = get_available_blueprints()

    if name in available_blueprints:
        return load_blueprint(available_blueprints[name])

    raise Exception("Can't load blueprint {} by name".format(name))

class BluePrint(object):
    """Class representing instructions for how to build a package. Expected to
    be constructed from a file, and will be used to create a Builder to build
    the package."""

    def __init__(self, name):
        self.name = name
        self.direct_dependencies = []
        self._full_dependencies = None

    @property
    def full_dependencies(self):
        """All dependencies, both direct and indirect. To avoid calculating
        every time, cache the result of the initial tree walk."""

        if not self._full_dependencies:
            self._full_dependencies = self.find_full_dependencies()

        return self._full_dependencies

    def find_full_dependencies(self):
        """Find all indirect dependencies, by finding dependencies of 
        dependencies."""

        full_dependencies = []
        modules = self.direct_dependencies

        while modules:
            module = modules.pop()
            full_dependencies.append(module)
            bp_dep = load_blueprint_by_name(module)
            modules += bp_dep.direct_dependencies

        return full_dependencies

LOADERS = { '.yaml' : load_blueprint_yaml }

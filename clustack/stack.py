import os

import yaml

import settings
from envmanager import EnvManager
from yamlbuilder import yaml_builders_in_path
from component import load_component_by_name

def get_dependency_tree(name):
    """Given the name of a builder, return its dependency tree. Each node of
    the tree is the name of a builder, and each of its children is a dependency.
    """

    rootrep = yaml_rep_by_name(name)

def dependencies_from_rep(yaml_rep):
    """Given yaml representation, return dependencies."""

    if 'dependencies' in yaml_rep:
        return yaml_rep['dependencies']
    else:
        return None

def yaml_rep_from_file(filename):
    """Read file and return parsed yaml."""

    with open(filename) as f:
        yaml_rep = yaml.load(f)

    return yaml_rep
        
def yaml_rep_by_name(name):
    """Given a name, return a yaml rep for the builder of that name, or None
    if it is unavailable"""

    yaml_dir = settings.yaml_dir
    yaml_ext = settings.yaml_ext

    name = name.lower()

    if name in yaml_builders_in_path(yaml_dir):
        filename = os.path.join(yaml_dir, name + yaml_ext)
        return yaml_rep_from_file(filename)
    else:
        return None

def load_stack_by_name(name):
    filename = name + settings.yaml_ext
    
    full_path = os.path.join(settings.stack_dir, filename)

    with open(full_path) as f:
        stack_yaml_rep = yaml.load(f)

    st = Stack()

    for component_name in stack_yaml_rep['components']:
        component = load_component_by_name(component_name)
        st.add_component(component)

    return st

class Stack(object):

    def __init__(self):
        self.env_manager = EnvManager()
        self.included_components = {}

    def add_component(self, component):

        if component.name in self.included_components:
            return

        self.included_components[component.name] = component

        component.update_stack(self)

        for dependency in component.direct_dependencies:
            c_dep = load_component_by_name(dependency)
            self.add_component(c_dep)

    def shell(self):
        self.env_manager.shell()

    def __repr__(self):
        return "<Stack: {}>".format(','.join(self.included_components))
        

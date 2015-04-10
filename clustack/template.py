"""Variable substitution with templates."""

import sys

import yaml
from jinja2 import FileSystemLoader, Environment, Template

from shelf import Shelf
import settings

def load_templated_yaml_rep(name, all_packages=None):

    name = name.lower()

    tloader = FileSystemLoader(settings.yaml_dir)
    tenv = Environment(loader=tloader)

    blueprint_name = name + settings.yaml_ext

    t = tenv.get_template(blueprint_name)

    s = Shelf()
    if all_packages is None:
        all_packages = s.installed_packages

    loaded_packages = {name: s.find_package(name) for name in all_packages}
    t_rendered = t.render(packages=loaded_packages)

    return yaml.load(t_rendered)

    
def templateit(name):

    print load_templated_yaml_rep(name)

def main():
    name = sys.argv[1]

    templateit(name)

if __name__ == '__main__':
    main()

"""Variable substitution with templates."""

import sys

import yaml
from jinja2 import FileSystemLoader, Environment, Template

import settings

def load_templated_yaml_rep(name, all_packages):

    name = name.lower()

    tloader = FileSystemLoader(settings.yaml_dir)
    tenv = Environment(loader=tloader)

    blueprint_name = name + settings.yaml_ext

    t = tenv.get_template(blueprint_name)

    t_rendered = t.render(packages=all_packages)

    return yaml.load(t_rendered)

    
def templateit(name):

    print load_templated_yaml_rep(name)

def main():
    name = sys.argv[1]

    templateit(name)

if __name__ == '__main__':
    main()

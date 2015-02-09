"""Variable substitution with templates."""

import sys

import yaml
from jinja2 import FileSystemLoader, Environment, Template

from component import load_component_by_name

def templateit(name):

    p = load_component_by_name('htslib')

    all_packages = {'htslib' : p}

    tloader = FileSystemLoader('yaml/')

    tenv = Environment(loader=tloader)

    t = tenv.get_template('samtools.yaml')

    rendered = t.render(packages=all_packages)

    print yaml.load(rendered)

def main():
    name = sys.argv[1]

    templateit(name)

if __name__ == '__main__':
    main()
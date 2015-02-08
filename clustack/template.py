"""Variable substitution with templates."""

import sys

from jinja2 import Template

from component import load_component_by_name

def templateit(name):

    p = load_component_by_name('htslib')

    all_packages = {'htslib' : p}

    t = Template("make HTSDIR={{ packages.htslib.include_dir }}")

    print t.render(packages=all_packages)

def main():
    name = sys.argv[1]

    templateit(name)

if __name__ == '__main__':
    main()
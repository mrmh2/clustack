"""Clustack component for dealing with modules"""

from jinja2 import FileSystemLoader, Environment, Template

import settings
from shelf import Shelf

def stuff(package_name):
    s = Shelf()

    if package_name not in s.installed_packages:
        raise Exception('Package {} not installed'.format(package_name))

    tloader = FileSystemLoader(settings.template_dir)
    tenv = Environment(loader=tloader)

    t = tenv.get_template(settings.module_template)

    print t.render(package=s.installed_packages[package_name])



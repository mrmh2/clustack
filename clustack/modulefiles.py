"""Clustack component for dealing with modules"""

import os

from jinja2 import FileSystemLoader, Environment, Template

import settings
from shelf import Shelf

def get_modulefile_path(package_name):
    """Generate the modulefile path from module name"""

    s = Shelf()

    if package_name not in s.installed_packages:
        raise Exception('Package {} not installed'.format(package_name))

    package = s.find_package(package_name)

    name = package.name
    version = package.version

    return os.path.join(settings.module_dir, name, version)

def generate_modulefile_text(package_name):
    """Given an installed package, generate the modulefile text necessary to
    activate that package."""

    s = Shelf()

    if package_name not in s.installed_packages:
        raise Exception('Package {} not installed'.format(package_name))

    tloader = FileSystemLoader(settings.template_dir)
    tenv = Environment(loader=tloader)

    t = tenv.get_template(settings.module_template)

    package = s.find_package(package_name)

    return t.render(package=package)



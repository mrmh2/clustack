"""Command line interface to clustack system for building software for clusters.
"""

import os
import sys
import inspect
import argparse
import importlib

from builder import Builder
from create import generate_yaml_builder
from utils import sys_command, safe_mkdir
import settings
from yamlbuilder import builder_by_name_yaml
from shelf import Shelf
from modulefiles import generate_modulefile_text, get_modulefile_path

from install import install_package

package_dir = os.path.join(os.getcwd(), "clustack/packages")

def pretty_columnular_output(list_of_strings, padding=2):
    """Output a list of strings in nicely formatted columns."""

    col_width = max(len(s) for s in list_of_strings) + padding

    print "".join(s.ljust(col_width) for s in list_of_strings)


def list_installed_packages(args):

    s = Shelf()

    package_names = s.installed_packages.keys()

    package_names.sort()

    #print '\t'.join(package_names)
    pretty_columnular_output(package_names)

def available_packages(args):

    yaml_ext = settings.yaml_ext

    all_files = os.listdir(settings.yaml_dir)

    split_names = [os.path.splitext(f) for f in all_files]

    builder_files = [name for name, ext in split_names if ext == yaml_ext]

    builder_files.sort()

    print '\t'.join(builder_files)

def install_from_import(args):

    module = importlib.import_module(args.name)

    # FIXME - better way to do this 
    other_classes = ["Builder", "BuildDir"]
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            if name not in other_classes:
                loaded_builder = obj()
                loaded_builder.install()

def install_package_cli(args):

    name = args.name

    install_package(name)
    
def create_builder(args):

    generate_yaml_builder(args.name, args.url)

def edit_builder(args):
    name = args.name

    builder_dir = settings.package_dir

    filename = name.lower() + '.py'

    full_path_name = os.path.join(builder_dir, filename)

    sys_command(['vim', full_path_name])

def show_modulefile(args):
    package_name = args.name

    print generate_modulefile_text(package_name)


def write_modulefile(args):
    package_name = args.name
    
    full_path = get_modulefile_path(package_name)

    dirname, filename = os.path.split(full_path)

    safe_mkdir(dirname)

    with open(full_path, 'w') as f:
        file_text = generate_modulefile_text(package_name)
        f.write(file_text)

def main():

    parser = argparse.ArgumentParser(description=__doc__)

    subparsers = parser.add_subparsers(help='sub-command help', 
                                        dest='subparser_name')

    parser_list = subparsers.add_parser('avail', help='List available software')
    parser_list.set_defaults(func=available_packages)

    parser_list = subparsers.add_parser('list', help='List installed software')
    parser_list.set_defaults(func=list_installed_packages)

    parser_install = subparsers.add_parser('install', help='Install a package')
    parser_install.add_argument('name')
    parser_install.set_defaults(func=install_package_cli)

    parser_create = subparsers.add_parser('create', help='Create a builder')
    parser_create.add_argument('name')
    parser_create.add_argument('url')
    parser_create.set_defaults(func=create_builder)

    parser_edit = subparsers.add_parser('edit', help='Edit a builder')
    parser_edit.add_argument('name')
    parser_edit.set_defaults(func=edit_builder)

    parser_module = subparsers.add_parser('module', help='Manage modulefiles')
    module_subparsers = parser_module.add_subparsers(help='module subcommand help',
                                                     dest='module_subparser_name')

    module_show = module_subparsers.add_parser('show', help='Show modulefile text')
    module_show.add_argument('name')
    module_show.set_defaults(func=show_modulefile)

    module_write = module_subparsers.add_parser('write', help='Write modulefile')
    module_write.add_argument('name')
    module_write.set_defaults(func=write_modulefile)

    args = parser.parse_args()

    args.func(args)

if __name__ == "__main__":
    main()

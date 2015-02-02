"""Command line interface to clustack system for building software for clusters.
"""

import os
import sys
import inspect
import argparse
import importlib

from clustack.builder import Builder
from clustack.create import generate_yaml_builder
from clustack.utils import sys_command
from clustack import settings
from clustack.yamlbuilder import builder_by_name_yaml

package_dir = os.path.join(os.getcwd(), "clustack/packages")

def list_packages(args):

    all_files = os.listdir(package_dir)

    split_names = [os.path.splitext(f) for f in all_files]

    builder_files = [name for name, ext in split_names if ext == '.py']

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

def install_package(args):

    name = args.name

    #yaml_path = os.path.join('yaml', name + '.yaml')

    yaml_builder = builder_by_name_yaml(name)

    yaml_builder.process_all_stages()
    
def create_builder(args):

    generate_yaml_builder(args.name, args.url)

def edit_builder(args):
    name = args.name

    builder_dir = settings.package_dir

    filename = name.lower() + '.py'

    full_path_name = os.path.join(builder_dir, filename)

    sys_command(['vim', full_path_name])


def main():

    parser = argparse.ArgumentParser(description=__doc__)

    subparsers = parser.add_subparsers(help='sub-command help', 
                                        dest='subparser_name')

    parser_list = subparsers.add_parser('list', help='List available software')
    parser_list.set_defaults(func=list_packages)

    parser_install = subparsers.add_parser('install', help='Install a package')
    parser_install.add_argument('name')
    parser_install.set_defaults(func=install_package)

    parser_create = subparsers.add_parser('create', help='Create a builder')
    parser_create.add_argument('name')
    parser_create.add_argument('url')
    parser_create.set_defaults(func=create_builder)

    parser_edit = subparsers.add_parser('edit', help='Edit a builder')
    parser_edit.add_argument('name')
    parser_edit.set_defaults(func=edit_builder)

    args = parser.parse_args()

    args.func(args)

if __name__ == "__main__":
    main()

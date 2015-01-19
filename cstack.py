"""Command line interface to clustack system for building software for clusters.
"""

import os
import sys
import inspect
import argparse
import importlib

from clustack.builder import Builder

package_dir = os.path.join(os.getcwd(), "clustack/packages")

def list_packages(args):

    print os.listdir(package_dir)

def install_package(args):

    module = importlib.import_module(args.name)

    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            if name is not "Builder":
                loaded_builder = obj()
                loaded_builder.install()
    

def main():

    parser = argparse.ArgumentParser(description=__doc__)

    subparsers = parser.add_subparsers(help='sub-command help', 
                                        dest='subparser_name')

    parser_list = subparsers.add_parser('list', help='List available software')
    parser_list.set_defaults(func=list_packages)

    parser_install = subparsers.add_parser('install', help='Install a package')
    parser_install.add_argument('name')
    parser_install.set_defaults(func=install_package)

    args = parser.parse_args()

    args.func(args)

if __name__ == "__main__":
    main()

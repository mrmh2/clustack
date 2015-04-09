"""Shelf - the environment manager for clustack. A shelf contains installed
components."""

import os
import sys
from collections import defaultdict

import settings
from component import FileSystemLoader

class Shelf(object):

    def __init__(self, loader=None):

        if loader is None:
            loader = FileSystemLoader()
            self.base_path = loader.base_path

        self.loader = loader

    @property
    def installed_packages(self):

        package_names = os.listdir(self.base_path)

        all_packages = defaultdict(dict)

        for package_name in package_names:


            try:
                package_versions = os.listdir(os.path.join(self.base_path, 
                        package_name))
            except OSError:
                package_versions = []

            for package_version in package_versions:

                package_to_add = self.loader.load(package_name, package_version)
                all_packages[package_name][package_version] = package_to_add

        return all_packages

    def find_package(self, name, version=None):
        """Find the package with the given name. If found, return the highest
        version, if not found, return none."""

        available_packages = self.installed_packages

        if name in available_packages:
            available_versions = available_packages[name]

            if version == None:
                version = sorted(available_versions)[-1]

            package = available_versions[version]

            return package

        return None

    def find_all_dependencies(self, package_name):

        if package_name not in self.installed_packages:
            raise Exception('Cannot find package in shelf: {}'.format(package_name))

        all_dependencies = set([])

        packages_to_check = [package_name]

        while len(packages_to_check):
            package = self.find_package(packages_to_check.pop())
            if package is not None:
                all_dependencies |= set(package.direct_dependencies)
                packages_to_check += package.direct_dependencies

        return list(all_dependencies)


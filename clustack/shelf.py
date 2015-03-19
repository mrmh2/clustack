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

            package_versions = os.listdir(os.path.join(self.base_path, 
                    package_name))

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


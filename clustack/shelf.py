"""Shelf - the environment manager for clustack"""

import os

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

        packages = dict((name, self.loader.load(name))
                    for name in package_names)

        return packages

#    @property

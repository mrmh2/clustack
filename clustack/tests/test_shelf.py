"""Test the shelf module"""

import os
import unittest

from clustack.shelf import Shelf
import clustack.settings

class TestShelf(unittest.TestCase):

    def setUp(self):
        self.shelf_dir = clustack.settings.shelf_dir

    def test_shelf_base_path(self):
        s = Shelf()

        expected_dir = os.path.join(self.shelf_dir)

        self.assertEqual(expected_dir, s.base_path)

    def test_installed_packages(self):

        s = Shelf()

        packages = s.installed_packages

        self.assertIn('zlib', packages)
#    def test_

if __name__ == '__main__':
    unittest.main()



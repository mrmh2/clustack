"""Test the shelf module"""

import os
import unittest

from clustack.shelf import Shelf

class TestShelf(unittest.TestCase):

    def test_shelf_root_dir(self):
        s = Shelf()
        expected_dir = os.path.join(os.getcwd(), 'shelf')

        self.assertEqual(expected_dir, s.root_dir)

    def test_installed_packages(self):

        s = Shelf()

        packages = s.installed_packages

        self.assertIn('zlib', packages)
#    def test_

if __name__ == '__main__':
    unittest.main()



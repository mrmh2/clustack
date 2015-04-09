"""Tests for components."""

import os
import unittest

import clustack.settings
import clustack.component
from clustack.component import Package

class TestPackage(unittest.TestCase):

    def test_package_init(self):
        p = Package('zlib', '1.2.8', '/tmp')

        self.assertEqual(p.name, 'zlib')
        self.assertEqual(p.version, '1.2.8')

class TestFileSystemLoader(unittest.TestCase):

    def setUp(self):
        self.fsl = clustack.component.FileSystemLoader()
        self.shelf_dir = clustack.settings.shelf_dir

    def test_init(self):
        expected_path = self.shelf_dir
        self.assertEqual(expected_path, self.fsl.base_path)

    def test_load(self):
        zlib_package = self.fsl.load('zlib', '1.2.8')

        self.assertEqual(zlib_package.name, 'zlib')
        self.assertEqual(zlib_package.version, '1.2.8')

class TestPackageFromPath(unittest.TestCase):
    """Test the package_from_path function."""

    def setUp(self):
        package_path = os.path.join(os.getcwd(), 'shelf', 'zlib', '1.2.8')
        self.zlib_package = clustack.component.package_from_path(package_path)
        self.package_path = package_path

    def test_package_base_dir(self):
        expected_path = os.path.join(os.getcwd(), 'shelf', 'zlib', '1.2.8')

        self.assertEqual(expected_path, self.zlib_package.base_path)

    def test_name(self):
        self.assertEqual(self.zlib_package.name, 'zlib')

    def test_version(self):
        self.assertEqual(self.zlib_package.version, '1.2.8')

    def test_source_dir(self):
        source_dir = os.path.join(self.package_path, 'source')

        self.assertEqual(source_dir, self.zlib_package.source_dir)

    def test_bin_dir(self):
        bin_dir = os.path.join(self.package_path, 'x86_64', 'bin')
        self.assertEqual(bin_dir, self.zlib_package.bin_dir)

    def test_lib_dir(self):
        lib_dir = os.path.join(self.package_path, 'x86_64', 'lib')
        self.assertEqual(lib_dir, self.zlib_package.lib_dir)

    def test_include_dir(self):
        include_dir = os.path.join(self.package_path, 'x86_64', 'include')
        self.assertEqual(include_dir, self.zlib_package.include_dir)

        
# class TestComponents(unittest.TestCase):

#     def test_list_packages(self):
#         package_list = component.list_packages()

#         self.assertIn('zlib', package_list)

#     def test_load_all_packages(self):
#         package_dict = component.load_all_packages()

#         self.assertIn('zlib', package_dict)
#         self.assertEqual(package_dict['zlib'].version, '1.2.8')

if __name__ == "__main__":
    unittest.main()

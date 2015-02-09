"""Tests for components."""

import unittest
import component

class TestPackageFromPath(unittest.TestCase):

    def setUp(self):
        self.packages = component.package_from_filesystem('zlib')
        
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

"""Test the settings modules."""

import os
import unittest

import clustack.settings

class TestSettings(unittest.TestCase):

    def setUp(self):
        self.clustack_root = os.getcwd()

    def test_clustack_root(self):
        self.assertEqual(self.clustack_root, clustack.settings.clustack_root)

    def test_resource_dir(self):
        expected_dir = os.path.join(self.clustack_root, 'resources')
        self.assertEqual(expected_dir, clustack.settings.resource_dir)

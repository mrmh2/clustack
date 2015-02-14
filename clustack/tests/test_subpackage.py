"""Tests for subpackage."""

import unittest

class TestSubpackageImports(unittest.TestCase):

    def test_module_import(self):
        import clustack.subpackage

    def test_class_import(self):
        from clustack.subpackage import SubPackage

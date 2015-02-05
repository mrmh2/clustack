import os
import unittest

import settings

from stack import yaml_rep_by_name, dependencies_from_rep
from yamlbuilder import builder_by_name_yaml


class TestStackFunctions(unittest.TestCase):
    
    def test_yaml_settings(self):
        self.assertEqual(settings.yaml_ext, '.yaml')
    
    def test_stack_settings(self):
        stack_dir = os.path.join(os.getcwd(), 'stack')
        self.assertEqual(settings.stack_dir, stack_dir)

    def test_yaml_rep_by_name(self):
        yr = yaml_rep_by_name('zlib')
        
        self.assertEqual(yr['name'], 'zlib')

    def test_dependencies_from_rep(self):
        yr = yaml_rep_by_name('python')

        deps = dependencies_from_rep(yr)

        self.assertEqual(deps, ['openssl', 'readline'])


# We need to be able to load a yaml builder
class TestYamlBuilder(unittest.TestCase):

    def test_yaml_builder_load_nodeps(self):
        pybuilder = builder_by_name_yaml('python', load_dependencies=False)
        self.assertEqual(pybuilder.name, 'python')
        self.assertEqual(pybuilder.version, '2.7.8')
        self.assertEqual(pybuilder.dependencies, ['openssl', 'readline'])

# We need to be able to walk the whole dependency tree
class TestDepTree(unittest.TestCase):

    def test_get_dependency_tree(self):
        dt = get_dependency_tree('python')
        self.assertEqual(dt, 'um')
        

def main():
    unittest.main()

if __name__ == "__main__":
    main()


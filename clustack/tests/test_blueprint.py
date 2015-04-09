import unittest

import clustack.blueprint

class TestBluePrint(unittest.TestCase):

    def test_get_available_blueprints(self):
        avail = clustack.blueprint.get_available_blueprints()

        self.assertIn('zlib', avail)

    def test_load_blueprint_yaml(self):
        bp_zlib = clustack.blueprint.load_blueprint_yaml('yaml/zlib.yaml')

        self.assertEqual(bp_zlib.name, 'zlib')

    def test_load_blueprint(self):
        bp_zlib = clustack.blueprint.load_blueprint('yaml/zlib.yaml')

        self.assertEqual(bp_zlib.name, 'zlib')

    def test_load_blueprint_by_name(self):
        bp_python = clustack.blueprint.load_blueprint_by_name('python')

        self.assertEqual(bp_python.name, 'python')

        self.assertEqual(bp_python.direct_dependencies, ['openssl', 'readline', 
                                                         'zlib'])

    def test_full_dependencies(self):
        bp_python = clustack.blueprint.load_blueprint_by_name('python')

        expected_deps = ['zlib', 'readline', 'ncurses', 'openssl']
        
        self.assertEqual(bp_python.full_dependencies, expected_deps)

if __name__ == "__main__":
    unittest.main()

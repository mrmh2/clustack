import unittest

import blueprint

class TestBluePrint(unittest.TestCase):

    def test_get_available_blueprints(self):
        avail = blueprint.get_available_blueprints()

        self.assertIn('zlib', avail)

    def test_load_blueprint_yaml(self):
        bp_zlib = blueprint.load_blueprint_yaml('yaml/zlib.yaml')

        self.assertEqual(bp_zlib.name, 'zlib')

    def test_load_blueprint(self):
        bp_zlib = blueprint.load_blueprint('yaml/zlib.yaml')

        self.assertEqual(bp_zlib.name, 'zlib')

    def test_load_blueprint_by_name(self):
        bp_python = blueprint.load_blueprint_by_name('python')

        self.assertEqual(bp_python.name, 'python')

        self.assertEqual(bp_python.direct_dependencies, ['openssl', 'readline'])

    def test_full_dependencies(self):
        bp_python = blueprint.load_blueprint_by_name('python')

        expected_deps = ['readline', 'ncurses', 'openssl', 'perl']
        
        self.assertEqual(bp_python.full_dependencies, expected_deps)

if __name__ == "__main__":
    unittest.main()

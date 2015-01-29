import os
import tempfile
import unittest

import settings
from utils import BuildDir, extract_packed_name
from builder import Builder
from envmanager import EnvManager

initial_cwd = os.getcwd()

class BuildDirTestCase(unittest.TestCase):
    def runTest(self):
        tempdir = tempfile.mkdtemp()

        os.chdir(tempdir)

        expected_path = os.path.join(tempdir, 'build')

        with BuildDir():
            self.assertEqual(os.getcwd(), expected_path)

class BuilderPathTests(unittest.TestCase):

    def setUp(self):
        self.testBuilder = Builder('zlib', 'http://zlib.net/zlib-1.2.8.tar.gz')
        self.testBuilder._version = '1.2.8'

    def test_name_and_version(self):

        self.assertEqual(self.testBuilder.name, 'zlib')
        self.assertEqual(self.testBuilder.version, '1.2.8')

    def test_shelf_dir(self):
        expected_dir = os.path.join(initial_cwd, 'shelf', 'zlib', '1.2.8')
        self.assertEqual(self.testBuilder.shelf_dir, expected_dir)

    def test_archive_dir(self):
        expected_dir = os.path.join(initial_cwd, 'shelf', 'zlib', '1.2.8', 'archive')
        self.assertEqual(self.testBuilder.archive_dir, expected_dir)

    def test_source_dir(self):
        expected_dir = os.path.join(initial_cwd, 'shelf', 'zlib', '1.2.8', 'source')
        self.assertEqual(self.testBuilder.source_dir, expected_dir)

    def test_build_dir(self):
        expected_dir = os.path.join(initial_cwd, 'shelf', 'zlib', '1.2.8', 'build')
        self.assertEqual(self.testBuilder.build_dir, expected_dir)

    def test_install_dir(self):
        expected_dir = os.path.join(initial_cwd, 'shelf', 'zlib', '1.2.8', 'x86_64')
        self.assertEqual(self.testBuilder.install_dir, expected_dir)

class BuilderBasicsTestCase(unittest.TestCase):

    def setUp(self):
        self.testBuilder = Builder('zlib', 'http://zlib.net/zlib-1.2.8.tar.gz')
        self.testBuilder._version = '1.2.8'

    def test_packed_name(self):
        self.assertEqual(self.testBuilder.packed_name, 'zlib-1.2.8.tar.gz')

    def test_archive_file_path(self):
        expected_path = os.path.join(initial_cwd, 'shelf', 'zlib', '1.2.8',
                                     'archive', 'zlib-1.2.8.tar.gz')
        self.assertEqual(self.testBuilder.archive_file_path, expected_path)

class SettingsTestCase(unittest.TestCase):

    def test_shelf_dir(self):
        expected_dir = os.path.join(initial_cwd, 'shelf')
        self.assertEqual(settings.shelf_dir, expected_dir)

class EnvManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.env_manager = EnvManager()

class UtilFunctionsTestCase(unittest.TestCase):

    def test_extract_packed_name(self):
        packed_name = extract_packed_name('http://zlib.net/zlib-1.2.8.tar.gz')

        self.assertEqual(packed_name, 'zlib-1.2.8.tar.gz')
    
def main():
    unittest.main()

if __name__ == "__main__":
    main()

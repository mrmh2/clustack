import os
import tempfile
import unittest

from utils import BuildDir
from builder import Builder

initial_cwd = os.getcwd()

class BuildDirTestCase(unittest.TestCase):
    def runTest(self):
        tempdir = tempfile.mkdtemp()

        os.chdir(tempdir)

        expected_path = os.path.join(tempdir, 'build')

        with BuildDir():
            self.assertEqual(os.getcwd(), expected_path)

class BuilderPathTests(unittest.TestCase):
    def runTest(self):
        testBuilder = Builder('zlib', 'http://zlib.net/zlib-1.2.8.tar.gz')
        testBuilder._version = '1.2.8'

        self.assertEqual(testBuilder.name, 'zlib')
        self.assertEqual(testBuilder.version, '1.2.8')

        expected_dir = os.path.join(initial_cwd, 'shelf', 'zlib', '1.2.8')
        self.assertEqual(testBuilder.shelf_dir, expected_dir)

        expected_dir = os.path.join(initial_cwd, 'shelf', 'zlib', '1.2.8', 'archive')
        self.assertEqual(testBuilder.archive_dir, expected_dir)

        expected_dir = os.path.join(initial_cwd, 'shelf', 'zlib', '1.2.8', 'source')
        self.assertEqual(testBuilder.source_dir, expected_dir)

        expected_dir = os.path.join(initial_cwd, 'shelf', 'zlib', '1.2.8', 'build')
        self.assertEqual(testBuilder.build_dir, expected_dir)

        expected_dir = os.path.join(initial_cwd, 'shelf', 'zlib', '1.2.8', 'x86_64')
        self.assertEqual(testBuilder.install_dir, expected_dir)


def test_builddir():

    tempdir = tempfile.mkdtemp()

    os.chdir(tempdir)

    with BuildDir():
        print os.getcwd()

def test_constructor():
    testBuilder = Builder("zlib", 'http://zlib.net/zlib-1.2.8.tar.gz')

# Expectation: shelf_dir

def test_shelf_dir():
    testBuilder = Builder("zlib", 'http://zlib.net/zlib-1.2.8.tar.gz')

    shelf_dir = testBuilder.shelf_dir
    expected_dir = os.path.join(os.getcwd(), 'shelf', 'zlib')

    assert shelf_dir == expected_dir
    
    
def test_builder():
    test_constructor()

    test_shelf_dir()
    
def main():
    #test_builddir()
    #test_builder()
    unittest.main()

if __name__ == "__main__":
    main()

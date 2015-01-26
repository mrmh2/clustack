import os
import tempfile
import unittest

from utils import BuildDir

class BuildDirTestCase(unittest.TestCase):
    def runTest(self):
        tempdir = tempfile.mkdtemp()

        os.chdir(tempdir)

        expected_path = os.path.join(tempdir, 'build')

        with BuildDir():
            self.assertEqual(os.getcwd(), expected_path)

def test_builddir():

    tempdir = tempfile.mkdtemp()

    os.chdir(tempdir)

    with BuildDir():
        print os.getcwd()
    
def main():
    test_builddir()

if __name__ == "__main__":
    unittest.main()

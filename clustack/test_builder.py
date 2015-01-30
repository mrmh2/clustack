import shutil
import tempfile
import unittest

from builder import Builder
import settings

class BuilderStageTestCase(unittest.TestCase):

    def setUp(self):
        self.testBuilder = Builder('zlib', 'http://zlib.net/zlib-1.2.8.tar.gz')
        self.testBuilder._version = '1.2.8'
        self.temp_shelf_dir = tempfile.mkdtemp()
        # FIXME - global settings are ugly here
        settings.shelf_dir = self.temp_shelf_dir

    def test_check_stage_allowed(self):
        with self.assertRaises(NameError):
            self.testBuilder.check_stage_finished("SOMETHING")

    def test_check_downloaded(self):
        self.assertFalse(self.testBuilder.check_stage_finished("DOWNLOAD"))

        self.testBuilder.download()

        self.assertTrue(self.testBuilder.check_stage_finished("DOWNLOAD"))

        self.assertFalse(self.testBuilder.check_stage_finished("UNPACK"))

        self.testBuilder.unpack()

        self.assertTrue(self.testBuilder.check_stage_finished("UNPACK"))

    def tearDown(self):
        shutil.rmtree(self.temp_shelf_dir)

def main():
    unittest.main()

if __name__ == "__main__":
    main()

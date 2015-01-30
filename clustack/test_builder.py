import os
import shutil
import tempfile
import unittest
import subprocess

from builder import Builder
import settings

class BuilderStageTestCase(unittest.TestCase):

    def setUp(self):
        # self.testBuilder = Builder('zlib', 'http://zlib.net/zlib-1.2.8.tar.gz')
        # self.testBuilder._version = '1.2.8'
        self.testBuilder = Builder('jpeg', 'http://www.ijg.org/files/jpegsrc.v8d.tar.gz')
        self.testBuilder._version = 'v8d'

        self.temp_shelf_dir = tempfile.mkdtemp()
        # FIXME - global settings are ugly here
        settings.shelf_dir = self.temp_shelf_dir

    def test_check_stage_allowed(self):
        with self.assertRaises(NameError):
            self.testBuilder.check_stage_finished("SOMETHING")

    def test_all_stages(self):
        self.assertFalse(self.testBuilder.check_stage_finished("DOWNLOAD"))

        self.testBuilder.download()

        self.assertTrue(self.testBuilder.check_stage_finished("DOWNLOAD"))

        self.assertFalse(self.testBuilder.check_stage_finished("UNPACK"))

        self.testBuilder.unpack()

        self.assertTrue(self.testBuilder.check_stage_finished("UNPACK"))

        self.testBuilder.configure()

        self.assertTrue(self.testBuilder.check_stage_finished("CONFIGURE"))

        self.testBuilder.build()

        jpeg_path = os.path.join(self.testBuilder.build_dir, 'libjpeg.la')
        self.assertTrue(os.path.exists(jpeg_path))

        self.testBuilder.install()
        self.assertTrue(self.testBuilder.check_stage_finished("INSTALL"))

        cjpeg_path = os.path.join(self.testBuilder.install_dir, 'bin', 'cjpeg')
        self.assertTrue(os.path.exists(cjpeg_path))

        returncode = subprocess.call([cjpeg_path, '--help'])
        self.assertEqual(returncode, 1)

    def tearDown(self):
        shutil.rmtree(self.temp_shelf_dir)

def main():
    unittest.main()

if __name__ == "__main__":
    main()

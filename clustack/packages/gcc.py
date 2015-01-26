import os

from clustack.builder import Builder
from clustack.utils import safe_mkdir, BuildDir

class gccBuilder(Builder):
    def __init__(self):
        self.url = 'http://ftpmirror.gnu.org/gcc/gcc-4.9.2/gcc-4.9.2.tar.bz2'
        self.name = 'gcc'
        self._version = '4.9.2'

    def build(self):
        safe_mkdir(self.own_shelf_dir)

        os.chdir(self.full_unpack_dir)

        with BuildDir():
           self.env_manager.run_command(['../configure', 
                                         '--prefix={}'.format(self.own_shelf_dir),
                                         '--disable-multilib'])
           self.env_manager.run_command(['make', 'bootstrap'])

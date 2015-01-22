import os

from clustack.builder import Builder
from clustack.utils import safe_mkdir, sys_command

class HTSLibBuilder(Builder):

    def __init__(self):
        self.url = 'https://github.com/samtools/htslib/archive/1.1.tar.gz'
        self.name = 'htslib'
        self._version = "1.1"

    def build(self):
        safe_mkdir(self.own_shelf_dir)

        os.chdir(self.full_unpack_dir)

        sys_command(['make'])
        sys_command(['make', 'install', 'prefix={}'.format(self.own_shelf_dir)])


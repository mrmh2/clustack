import os

from clustack.builder import Builder
from clustack.utils import safe_mkdir, sys_command

class SamtoolsBuilder(Builder):
    def __init__(self):
        self.url = 'https://github.com/samtools/samtools/archive/1.1.tar.gz'
        self.name = 'samtools'
        self._version = '1.1'

    def build(self):
        safe_mkdir(self.own_shelf_dir)

        os.chdir(self.full_unpack_dir)

        sys_command(['make'])



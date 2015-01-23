from clustack.builder import Builder

class libpngBuilder(Builder):
    def __init__(self):
        self.url = 'https://downloads.sf.net/project/libpng/libpng16/1.6.15/libpng-1.6.15.tar.xz'
        self.name = 'libpng'
        self._version = '1.6.15'


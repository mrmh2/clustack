from clustack.builder import Builder

class ZlibBuilder(Builder):
    def __init__(self):
        self.url = 'http://zlib.net/zlib-1.2.8.tar.gz'
        self.name = 'zlib'
        self._version = '1.2.8'

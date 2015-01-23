from clustack.builder import Builder

class freetypeBuilder(Builder):
    def __init__(self):
        self.url = 'https://downloads.sf.net/project/freetype/freetype2/2.5.3/freetype-2.5.3.tar.bz2'
        self.name = 'freetype'
        self._version = '2.5.3'


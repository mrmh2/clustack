from clustack.builder import Builder

class M4Builder(Builder):
    def __init__(self):
        self.url = 'http://ftpmirror.gnu.org/m4/m4-1.4.17.tar.xz'
        self.name = 'm4'
        self._version = '1.4.17'

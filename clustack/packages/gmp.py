from clustack.builder import Builder

class GMPBuilder(Builder):
    def __init__(self):
        self.url = 'http://ftpmirror.gnu.org/gmp/gmp-6.0.0a.tar.bz2'
        self.name = 'gmp'
        self._version = '6.0.0'

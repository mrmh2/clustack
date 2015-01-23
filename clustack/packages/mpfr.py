from clustack.builder import Builder

class MPFRBuilder(Builder):
    def __init__(self):
        self.url = 'http://ftpmirror.gnu.org/mpfr/mpfr-3.1.2.tar.bz2'
        self.name = 'mpfr'
        self._version = '3.1.2'

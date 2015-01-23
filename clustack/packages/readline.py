from clustack.builder import Builder

class readline(Builder):
    def __init__(self):
        self.url = 'http://ftpmirror.gnu.org/readline/readline-6.3.tar.gz'
        self.name = 'readline'
        self._version = '6.3'

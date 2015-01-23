from clustack.builder import Builder

class pixmanBuilder(Builder):
    def __init__(self):
        self.url = 'http://cairographics.org/releases/pixman-0.32.6.tar.gz'
        self.name = 'pixman'
        self._version = '0.32.6'


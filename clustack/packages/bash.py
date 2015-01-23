from clustack.builder import Builder

class bashBuilder(Builder):
    def __init__(self):
        self.url = 'http://ftpmirror.gnu.org/bash/bash-4.3.tar.gz'
        self.name = 'bash'
        self._version = '4.3'

from clustack.builder import Builder

class jpegBuilder(Builder):
    def __init__(self):
        self.url = 'http://www.ijg.org/files/jpegsrc.v8d.tar.gz'
        self.name = 'jpeg'
        self._version = 'v8d'


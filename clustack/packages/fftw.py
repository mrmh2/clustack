from clustack.builder import Builder

class fftwBuilder(Builder):
    def __init__(self):
        self.url = 'http://www.fftw.org/fftw-3.3.4.tar.gz'
        self.name = 'fftw'
        self._version = '3.3.4'


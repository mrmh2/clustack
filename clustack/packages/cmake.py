from clustack.builder import Builder

class CMakeBuilder(Builder):

    def __init__(self):
        self.url = 'http://www.cmake.org/files/v3.0/cmake-3.0.2.tar.gz'
        self.name = 'cmake'

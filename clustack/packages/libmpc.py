from clustack.builder import Builder

class libMPCBuilder(Builder):
    def __init__(self):
        self.url = 'http://ftpmirror.gnu.org/mpc/mpc-1.0.2.tar.gz'
        self.name = 'mpc'
        self._version = '1.0.2'

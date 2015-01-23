from clustack.builder import Builder

class xorgxserverBuilder(Builder):
    def __init__(self):
        self.url = 'http://www.x.org/releases/X11R7.7/src/xserver/xorg-server-1.12.2.tar.bz2'
        self.name = 'xorg-xserver'
        self._version = '1.12.2'


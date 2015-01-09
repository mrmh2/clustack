import os
import sys
import errno
import urllib
import subprocess

from builder import Builder



def make_structure():


    root_path = os.getcwd()

    shelf_dir = os.path.join(root_path, 'shelf')
    target_dir = os.path.join(shelf_dir, 'xz', '5.0.7')
    bin_dir = os.path.join(root_path, 'bin')

    safe_mkdir(bin_dir)
    safe_mkdir(cache_dir)
    safe_mkdir(target_dir)

def download(url):

    os.chdir(cache_dir)

    sys_command(['wget', url])

def download_and_save(url, filename):
    
    urllib.urlretrieve(url, filename)

def download_and_build(url):

    os.chdir(cache_dir)

    sys_command(['wget', url])

    sys_command(['tar', '-xvjf', 'xz-5.0.7.tar.bz2'])

    os.chdir('xz-5.0.7')

    sys_command(['./configure', '--prefix={}'.format(target_dir)])

    sys_command(['make', 'install'])

    target_to_link = os.path.join(target_dir, 'bin', 'xz')
    dest_link = os.path.join(bin_dir, 'xz')

    safe_symlink(target_to_link, dest_link)

def string_after(string, character):
    return string.split(character)[1]

def string_before(string, character):
    return string.split(character)[0]

def string_between(string, start_char, end_char):

    return string_after(string_before(string, end_char), start_char)



class CMakeBuilder(Builder):

    def __init__(self):
        self.url = 'http://www.cmake.org/files/v3.0/cmake-3.0.2.tar.gz'
        self.name = 'cmake'

class PythonBuilder(Builder):
    def __init__(self):
        self.url = "https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz"
        self.name = 'python'

class BamToolsBuilder(Builder):
    def __init__(self):
        self.url = "https://github.com/pezmaster31/bamtools/archive/v2.3.0.tar.gz"
        self.name = 'bamtools'
        self._version = '2.3.0'

class ZlibBuilder(Builder):
    def __init__(self):
        self.url = 'http://zlib.net/zlib-1.2.8.tar.gz'
        self.name = 'zlib'
        self._version = '1.2.8'


def main():

    #LIBRARY_PATH
    #CPATH

    # zb = ZlibBuilder()
    # zb.install()

    # pb = PythonBuilder()
    # pb.install()

    bb = BamToolsBuilder()
    bb.install()

    #print bb.url

    #urllib.urlretrieve(bb.url, '2.3.0.tar.gz')

    #url = 'http://fossies.org/linux/misc/xz-5.0.7.tar.bz2'

    # pbuilder.cached_fetch()
    # pbuilder.unpack()
    # pbuilder.build()

    #pbuilder.link()

    # url = 'https://pypi.python.org/packages/source/s/setuptools/setuptools-5.4.2.tar.gz'
    # name = 'setuptools'

    # sbuilder = Builder(name, url)

    # sbuilder.cached_fetch()
    # sbuilder.unpack()

    # print sbuilder.full_unpack_dir

    # cm = CMakeBuilder()
    # cm.install()

    pass


if __name__ == "__main__":
    main()


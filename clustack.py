import os
import sys
import errno
import urllib
import subprocess

bin_dir = os.path.join(os.getcwd(), 'bin')
include_dir = os.path.join(os.getcwd(), 'include')
lib_dir = os.path.join(os.getcwd(), 'lib')
cache_dir = '.cache'
shelf_dir = os.path.join(os.getcwd(), 'shelf')

def safe_mkdir(dir_path):

    try:
        os.makedirs(dir_path)
    except OSError, e:
        if e.errno != errno.EEXIST:
            print "Error creating directory %s" % dir_path
            sys.exit(2)

def safe_symlink(link_from, link_to):
    try:

        os.symlink(link_from, link_to)
    except OSError, e:
        if e.errno != errno.EEXIST:
            print "Error symlinking: ", e
            sys.exit(2)

def sys_command(args):
    
#    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = subprocess.Popen(args)
    p.wait()

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

def extract_version(url):
    components = url.split('/')

    filename = components[-1]

    return string_between(filename, '-', '.tgz')

def extract_packed_name(url):
    components = url.split('/')

    filename = components[-1]

    return filename

class Builder(object):

    def __init__(self, name, url):
        self.name = name
        self.url = url

    @property
    def version(self):
        try:
            return self._version
        except AttributeError:
            self._version = extract_version(self.url)
            return self._version

    @property
    def packed_name(self):
        return extract_packed_name(self.url)

    @property
    def own_cache_dir(self):
        return os.path.join(cache_dir, self.name, self.version)

    @property
    def own_shelf_dir(self):
        return os.path.join(shelf_dir, self.name, self.version)

    def cached_fetch(self):
        safe_mkdir(self.source_dir)

        full_target_name = os.path.join(self.own_cache_dir, self.packed_name)

        if not os.path.exists(full_target_name):
            #sys_command(['curl', self.url, '-o', full_target_name])
            download_and_save(self.url, full_target_name)

    @property
    def source_dir(self):
        return os.path.join(self.own_cache_dir, 'source')

    def unpack(self):
        # pwd = os.getcwd()
        # os.chdir(self.source_dir)
        full_packed_name = os.path.join(self.own_cache_dir, self.packed_name)
        
        sys_command(['tar', '-xf', full_packed_name, '-C', self.source_dir])
        #os.chdir(pwd)

    @property
    def full_unpack_dir(self):
        unpack_dir = os.listdir(self.source_dir)[0]
        return os.path.join(self.source_dir, unpack_dir)

    def build(self):
        safe_mkdir(self.own_shelf_dir)

        os.chdir(self.full_unpack_dir)

        files = os.listdir(os.getcwd())

        if 'CMakeLists.txt' in files:
            safe_mkdir('build')
            os.chdir('build')
            cmake_flags = "-DCMAKE_INSTALL_PREFIX:PATH={}".format(self.own_shelf_dir)
            sys_command(['cmake', cmake_flags, '..'])
            self.env_manager.run_command(['make', 'install'])
        else:
            sys_command(['./configure', '--prefix={}'.format(self.own_shelf_dir)])
            sys_command(['make', 'install'])

    def link_from_subdir(self, subdir_name, dest_dir):
        """Link files in a particular subdirectory of the compiled package (e.g.
        bin, lib, include) into the overall equivalent directory"""

        safe_mkdir(dest_dir)

        shelf_path = os.path.join(self.own_shelf_dir, subdir_name)
        for file_to_link in os.listdir(shelf_path):
            link_from = os.path.join(shelf_path, file_to_link)
            link_to = os.path.join(dest_dir, file_to_link)

            safe_symlink(link_from, link_to)

    def link(self):

        self.link_from_subdir('lib', lib_dir)
        self.link_from_subdir('include', include_dir)

        # safe_mkdir(bin_dir)

    def install(self):
        self.env_manager = EnvManager()
        self.env_manager.set_variable('CPATH', include_dir)
        self.env_manager.set_variable('LIBRARY_PATH', lib_dir)

        self.cached_fetch()
        self.unpack()
        self.build()
        self.link()

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

class EnvManager(object):
    """Manage UNIX environment variables for specific building"""

    def __init__(self):
        self.start_env = os.environ.copy()
        self.path_list = []
        self.my_env = self.start_env
        #self.my_env = {'PATH': ''}

    def dump(self):
        print self.my_env

    def build_path(self):
        self.my_env["PATH"] = ':'.join(self.path_list)

    def add_path(self, path):
        self.path_list.append(path)
        self.build_path()

    def run_command(self, command):
        p = subprocess.Popen(command, env=self.my_env)
        p.wait()

    def set_variable(self, variable, value):
        self.my_env[variable] = value

def test_env_manager():

    myenv = EnvManager()

    myenv.add_path('/usr/bin')
    myenv.add_path('/bin')

    myenv.dump()

    myenv.run_command('ls')

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


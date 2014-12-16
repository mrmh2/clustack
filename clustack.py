import os
import sys
import errno
import subprocess

bin_dir = os.path.join(os.getcwd(), 'bin')
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
            sys_command(['curl', self.url, '-o', full_target_name])

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

        sys_command(['./configure', '--prefix={}'.format(self.own_shelf_dir)])
        sys_command(['make', 'install'])

    def link(self):
        safe_mkdir(bin_dir)

        shelf_bin_path = os.path.join(self.own_shelf_dir, 'bin')

        bin_to_link = 'python'

        link_from = os.path.join(shelf_bin_path, bin_to_link)
        link_to = os.path.join(bin_dir, bin_to_link)

        safe_symlink(link_from, link_to)

        
def main():

    #url = 'http://fossies.org/linux/misc/xz-5.0.7.tar.bz2'
    url = "https://www.python.org/ftp/python/2.7.8/Python-2.7.8.tgz"
    name = 'python'
    pbuilder = Builder(name, url)

    pbuilder.cached_fetch()
    pbuilder.unpack()
    pbuilder.build()

    pbuilder.link()

    # url = 'https://pypi.python.org/packages/source/s/setuptools/setuptools-5.4.2.tar.gz'
    # name = 'setuptools'

    # sbuilder = Builder(name, url)

    # sbuilder.cached_fetch()
    # sbuilder.unpack()

    # print sbuilder.full_unpack_dir


if __name__ == "__main__":
    main()


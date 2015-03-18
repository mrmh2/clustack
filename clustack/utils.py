import os
import sys
import errno
import urllib
import subprocess

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

def safe_mkdir(dir_path):

    try:
        os.makedirs(dir_path)
    except OSError, e:
        if e.errno != errno.EEXIST:
            print "Error creating directory %s" % dir_path
            sys.exit(2)

def sys_command(args):
    
#    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = subprocess.Popen(args)
    p.wait()

def download_and_save(url, filename):
    
    try:
        urllib.urlretrieve(url, filename)
    except IOError, e:
        print "Failed to open url: {}".format(url)
        print "Error was: {}".format(e)
        print "This may indicate that python was compiled without SSL support"
        sys.exit(2)



class BuildDir(object):
    """Create a named build directory for compilation, and change the current
    working directory to it. Save the old working directory to return to on
    exit"""

    def __init__(self, dir_name='build'):
        self.dir_name = dir_name
    
    def __enter__(self):
        self.store_cwd = os.getcwd()

        os.mkdir(self.dir_name)

        os.chdir(self.dir_name)

    def __exit__(self, type, value, traceback):

        os.chdir(self.store_cwd)
        
        

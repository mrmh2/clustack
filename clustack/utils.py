import os
import sys
import errno
import subprocess

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
        
        

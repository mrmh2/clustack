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

def safe_symlink(link_from, link_to):
    try:

        os.symlink(link_from, link_to)
    except OSError, e:
        if e.errno != errno.EEXIST:
            print "Error symlinking: ", e
            sys.exit(2)

def sys_command(args):
    
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()

def main():

    cache_dir = '.cache'

    root_path = os.getcwd()

    shelf_dir = os.path.join(root_path, 'shelf')
    target_dir = os.path.join(shelf_dir, 'xz', '5.0.7')
    bin_dir = os.path.join(root_path, 'bin')

    safe_mkdir(bin_dir)
    safe_mkdir(cache_dir)
    safe_mkdir(target_dir)


    os.chdir(cache_dir)

    url = 'http://fossies.org/linux/misc/xz-5.0.7.tar.bz2'
    
    sys_command(['wget', url])

    sys_command(['tar', '-xvjf', 'xz-5.0.7.tar.bz2'])

    os.chdir('xz-5.0.7')

    sys_command(['./configure', '--prefix={}'.format(target_dir)])

    sys_command(['make', 'install'])

    target_to_link = os.path.join(target_dir, 'bin', 'xz')
    dest_link = os.path.join(bin_dir, 'xz')

    safe_symlink(target_to_link, dest_link)

if __name__ == "__main__":
    main()


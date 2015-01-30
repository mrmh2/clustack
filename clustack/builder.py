import os
import sys
import errno
import shutil
import urllib
import tempfile
import subprocess

import utils
from utils import safe_mkdir, sys_command, extract_packed_name
import settings

from envmanager import EnvManager

# bin_dir = os.path.join(os.getcwd(), 'bin')
# include_dir = os.path.join(os.getcwd(), 'include')
# lib_dir = os.path.join(os.getcwd(), 'lib')
# cache_dir = '.cache'
# shelf_dir = os.path.join(os.getcwd(), 'shelf')

# def debug_break():
#     print("*** Break ***")
#     sys.exit(0)


# def string_after(string, character):
#     return string.split(character)[1]

# def string_before(string, character):
#     return string.split(character)[0]

# def string_between(string, start_char, end_char):

#     return string_after(string_before(string, end_char), start_char)

# def extract_version(url):
#     components = url.split('/')

#     filename = components[-1]

#     return string_between(filename, '-', '.tgz')

# def extract_packed_name(url):
#     components = url.split('/')

#     filename = components[-1]

#     return filename


# def safe_symlink(link_from, link_to):
#     try:

#         os.symlink(link_from, link_to)
#     except OSError, e:
#         if e.errno != errno.EEXIST:
#             print "Error symlinking: ", e
#             sys.exit(2)

builder_stages = [ "DOWNLOAD",
                   "UNPACK",
                   "CONFIGURE",
                   "BUILD",
                   "INSTALL",
                   "LINK" ]

class Builder(object):
    """

We expect to perform the following stages:

    download
    unpack
    configure
    build
    install
    link

Special directories:

    shelf_dir
    archive_dir
    source_dir
    install_dir
    build_dir

source and build are by default the same directory."""

    def __init__(self, name, url, build_in_source=True):
        self.name = name
        self.url = url
        self.build_in_source = build_in_source

        self.env_manager = EnvManager()
        # self.env_manager.set_variable('CPATH', include_dir)
        # self.env_manager.set_variable('LIBRARY_PATH', lib_dir)

    @property
    def shelf_dir(self):
        """Directory root for this package. Should be of the form:

        base_dir/package_name/package_version."""

        return os.path.join(settings.shelf_dir, self.name, self.version)

    @property
    def archive_dir(self):
        """Directory in which package tarball (or equivalent) will live. Of the
        form:

        base_dir/package_name/package_version/archive"""

        return os.path.join(self.shelf_dir, 'archive')

    @property
    def source_dir(self):
        """Directory in which uncompressed package source will live. Of the
        form:
        
        base_dir/package_name/package_version/source"""

        return os.path.join(self.shelf_dir, 'source')

    @property
    def build_dir(self):
        """Directory in which package will be built. Of the form:

        base_dir/package_name/package_version/build"""

        if self.build_in_source:
            return self.source_dir
        else:
            return os.path.join(self.shelf_dir, 'build')

    @property
    def install_dir(self):
        """Directory to which package will be installed. Of the form:

        base_dir/package_name/package_version/x86_64"""

        return os.path.join(self.shelf_dir, 'x86_64')

    @property
    def version(self):
        """If we've already set our version, return that. Otherwise, raise
        an exception"""

        try:
            return self._version
        except AttributeError:
            raise Exception('No version set')
        # try:
        #     return self._version
        # except AttributeError:
        #     self._version = extract_version(self.url)
        #     return self._version


    def check_stage_finished(self, stage_name):
        """Test to see whether the construction phase with the given name is
        finished."""

        if stage_name not in builder_stages:
            raise NameError('{} not a valid stage'.format(stage_name))

        if stage_name == "DOWNLOAD":
            
            return os.path.exists(self.archive_file_path)

        if stage_name == "UNPACK":
            if not os.path.exists(self.source_dir):
                return False

            if len(os.listdir(self.source_dir)):

                return True
            else:
                return False

        if stage_name == "CONFIGURE":
            
            makefile_path = os.path.join(self.build_dir, 'Makefile')
            return os.path.exists(makefile_path)

        if stage_name == "INSTALL":
            
            installed_files = os.listdir(self.install_dir)

            return len(installed_files) > 0

    @property
    def packed_name(self):
        """Return the name of the source tarball (or equivalent) used in the
        package"""

        return extract_packed_name(self.url)

    @property
    def archive_file_path(self):
        """Full path to archive file."""

        return os.path.join(self.archive_dir, self.packed_name)

    def system(self, command):
        """Run the given command using our internal managed environment"""

        return self.env_manager.run_command(command)

    def download(self):
        """Fetch the package source from its URL and save it in our source
        directory."""

        safe_mkdir(self.archive_dir)

        full_target_name = os.path.join(self.archive_dir, self.packed_name)

        utils.download_and_save(self.url, full_target_name)


    def unpack(self):
        """Unpack the source archive into the source directory. Because we don't
        know what directory name will be in the tarball, we unpack to a temporary
        directory and then move to the source directory."""

        if os.path.exists(self.source_dir):
            shutil.rmtree(self.source_dir)

        tmpdir = tempfile.mkdtemp()
        self.system(['tar', '-xf', self.archive_file_path, '-C', tmpdir])

        unpack_contents = os.listdir(tmpdir)

        if len(unpack_contents) == 1:
            unpack_path = os.path.join(tmpdir, unpack_contents[0])
        else:
            raise Exception('Multiple files in unpack directory')

        shutil.move(unpack_path, self.source_dir)


        # # Unpack only if we haven't done so already
        # if not len(os.listdir(self.source_dir)):
        #     sys_command(['tar', '-xf', full_packed_name, '-C', self.source_dir])

    def configure(self):
        """Configure build process."""

        if self.build_in_source:
            os.chdir(self.source_dir)
        else:
            safe_mkdir(self.build_dir)
            os.chdir(self.build_dir)

        source_root_files = os.listdir(self.source_dir)

        if 'configure' in source_root_files:
            self.system(['./configure', '--prefix={}'.format(self.install_dir)])
            return

        if 'CMakeLists.txt' in source_root_files:
            cmake_flags = "-DCMAKE_INSTALL_PREFIX:PATH={}".format(self.install_dir)
            self.system(['cmake', cmake_flags, '..'])
            return

        raise BuilderError('No configure strategy for this package')

    def build(self):
        """Build the software."""

        os.chdir(self.build_dir)

        self.system('make')

    def install(self):
        """Install to the builder's specified install directory"""

        os.chdir(self.build_dir)

        safe_mkdir(self.install_dir)

        self.system(['make', 'install'])

    # @property
    # def full_unpack_dir(self):
    #     unpack_dir = os.listdir(self.source_dir)[0]
    #     return os.path.join(self.source_dir, unpack_dir)

    # def build(self):
    #     safe_mkdir(self.own_shelf_dir)

    #     os.chdir(self.full_unpack_dir)

    #     files = os.listdir(os.getcwd())

    #     if 'CMakeLists.txt' in files:
    #         safe_mkdir('build')
    #         os.chdir('build')
    #         cmake_flags = "-DCMAKE_INSTALL_PREFIX:PATH={}".format(self.own_shelf_dir)
    #         self.env_manager.run_command(['cmake', cmake_flags, '..'])
    #         self.env_manager.run_command(['make', 'install'])
    #     else:
    #         self.env_manager.run_command(['./configure', '--prefix={}'.format(self.own_shelf_dir)])
    #         self.env_manager.run_command(['make', 'install'])

    # def link_from_subdir(self, subdir_name, dest_dir):
    #     """Link files in a particular subdirectory of the compiled package (e.g.
    #     bin, lib, include) into the overall equivalent directory"""

    #     safe_mkdir(dest_dir)

    #     shelf_path = os.path.join(self.own_shelf_dir, subdir_name)

    #     if not os.path.exists(shelf_path):
    #         return

    #     for file_to_link in os.listdir(shelf_path):
    #         link_from = os.path.join(shelf_path, file_to_link)
    #         link_to = os.path.join(dest_dir, file_to_link)

    #         safe_symlink(link_from, link_to)

    # def link(self):

    #     self.link_from_subdir('bin', bin_dir)
    #     self.link_from_subdir('lib', lib_dir)
    #     self.link_from_subdir('include', include_dir)

    #     # safe_mkdir(bin_dir)

    # def install(self):
    #     self.env_manager = EnvManager()
    #     self.env_manager.set_variable('CPATH', include_dir)
    #     self.env_manager.set_variable('LIBRARY_PATH', lib_dir)

    #     self.cached_fetch()
    #     self.unpack()
    #     self.build()
    #     self.link()

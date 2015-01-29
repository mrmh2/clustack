import os
import sys
import errno
import urllib
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
    build_dir"""

    def __init__(self, name, url):
        self.name = name
        self.url = url

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

        return os.path.join(self.shelf_dir, 'build')

    @property
    def install_dir(self):
        """Directory to which package will be installed. Of the form:

        base_dir/package_name/package_version/x86_64"""

        return os.path.join(self.shelf_dir, 'x86_64')

    @property
    def version(self):
        """If we've already set our version, return that. Otherwise, attempt to
        derive it from our url"""

        try:
            return self._version
        except AttributeError:
            self._version = extract_version(self.url)
            return self._version


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
            

    @property
    def packed_name(self):
        """Return the name of the source tarball (or equivalent) used in the
        package"""

        return extract_packed_name(self.url)

    @property
    def archive_file_path(self):
        """Full path to archive file."""

        return os.path.join(self.archive_dir, self.packed_name)

    # @property
    # def own_cache_dir(self):
    #     return os.path.join(cache_dir, self.name, self.version)

    # @property
    # def own_shelf_dir(self):
    #     """Path for installed files."""

    #     return os.path.join(shelf_dir, self.name, self.version)

    # @property
    # def source_dir(self):
    #     """Path to store source archive and unpacked source"""

    #     return os.path.join(self.own_cache_dir, 'source')

    def download(self):
        """Fetch the package source from its URL and save it in our source
        directory."""

        safe_mkdir(self.archive_dir)

        full_target_name = os.path.join(self.archive_dir, self.packed_name)

        utils.download_and_save(self.url, full_target_name)


    def unpack(self):
        """Unpack the source archive into the source directory."""

        safe_mkdir(self.source_dir)

        sys_command(['tar', '-xf', self.archive_file_path, '-C', self.source_dir])
        # full_packed_name = os.path.join(self.own_cache_dir, self.packed_name)

        # # Unpack only if we haven't done so already
        # if not len(os.listdir(self.source_dir)):
        #     sys_command(['tar', '-xf', full_packed_name, '-C', self.source_dir])

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

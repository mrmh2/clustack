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

def willlog(message):
    print message

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
    def include_dir(self):
        """Directory in which installed package headers live. Of the form:

        base_dir/package_name/package_version/x86_64/include"""

        return os.path.join(self.install_dir, 'include')

    @property
    def lib_dir(self):
        """Directory in which installed package libraries live. Of the form:

        base_dir/package_name/package_version/x86_64/lib"""

        return os.path.join(self.install_dir, 'lib')

    @property
    def pkgconfig_dir(self):
        """Directory in which pkg-config files exist, if any."""

        pkgconfig_dir = os.path.join(self.lib_dir, 'pkgconfig')

        if os.path.exists(pkgconfig_dir):
            return pkgconfig_dir
        else:
            return None

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
            willlog("Check unpack {}".format(self.name))
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

            try:
                installed_files = os.listdir(self.install_dir)
            except OSError, e:
                if e.errno == errno.ENOENT:
                    return False
                else:
                    raise

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

        # TODO logging
        return self.env_manager.run_command(command)

    def check_output(self, command):
        """Run the given command with our managed environment and return output"""

        return self.env_manager.check_output(command)

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

        if 'CMakeLists.txt' in os.listdir(self.source_dir):
            self.build_in_source = False

        # # Unpack only if we haven't done so already
        # if not len(os.listdir(self.source_dir)):
        #     sys_command(['tar', '-xf', full_packed_name, '-C', self.source_dir])

    def _configure(self):
        """Configure build process."""

        if self.build_in_source:
            os.chdir(self.source_dir)
        else:
            safe_mkdir(self.build_dir)
            os.chdir(self.build_dir)

        source_root_files = os.listdir(self.source_dir)

        try:
            configure_opts = self.configure_opts
        except AttributeError:
            configure_opts = ""

        if 'configure' in source_root_files:
            configure_command = ['./configure', '--prefix={}'.format(self.install_dir)]
            if configure_opts is not "":
                configure_command += ['{}'.format(configure_opts)]
            self.system(configure_command)
            return

        if 'CMakeLists.txt' in source_root_files:
            safe_mkdir(self.build_dir)
            os.chdir(self.build_dir)
            cmake_flags = "-DCMAKE_INSTALL_PREFIX:PATH={}".format(self.install_dir)
            self.system(['cmake', cmake_flags, self.source_dir])
            return

        if 'Makefile' in source_root_files:
            # We don't need to configure, hopefully
            return

        raise BuilderError('No configure strategy for this package')

    def configure(self):
        try:
            self.user_configure(self)
        except AttributeError:
            self._configure()

    def build(self):
        try:
            self.user_build(self)
        except AttributeError:
            self._build()

    def _build(self):
        """Build the software."""

        os.chdir(self.build_dir)

        self.system('make')

    def install(self):
        try:
            self.user_install(self)
        except AttributeError:
            self._install()
            
    def _install(self):
        """Install to the builder's specified install directory"""

        os.chdir(self.build_dir)

        safe_mkdir(self.install_dir)

        self.system(['make', 'install'])

    def process_all_stages(self):

        try:
            self.subpackage(self)
            return
        except AttributeError:
            pass

        if not self.check_stage_finished("DOWNLOAD"):
            self.download()
        if not self.check_stage_finished("UNPACK"):
            self.unpack()

        # TODO - this seems a nasty way to do this
        try:
            self.user_allscript(self)
        except AttributeError:
            self.configure()
            self.build()
            self.install()

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


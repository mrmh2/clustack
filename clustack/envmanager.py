import os
import sys
import subprocess

DEFAULT_PATHS = ['CPATH', 'LIBRARY_PATH', 'LD_LIBRARY_PATH', 'PKG_CONFIG_PATH']

class PathlikeVariable(object):
    """Manage variables like PATH, which have an ordered list of components from
    which items can be removed or added, and are represented in environments as
    a colon delimited string."""

    def  __init__(self, name, env):
        try:
            self.item_list = env[name].split(':')
        except KeyError:
            self.item_list = []
            
    def add_path(self, path):
        self.item_list.insert(0, path)

    def __str__(self):
        return ':'.join(self.item_list)
        
class EnvManager(object):
    """Manage UNIX environment variables for specific building."""

    def __init__(self, pathvars_to_manage=DEFAULT_PATHS):
        self.start_env = os.environ.copy()
        self.path_list = self.start_env['PATH'].split(':')
        self.my_env = self.start_env
        #self.cpath_list = self.init_pathlike_variable('CPATH')
        
        self.pathvars = {pathvar : PathlikeVariable(pathvar, self.my_env)
                         for pathvar in pathvars_to_manage}

    def add_to_pathvar(self, var_name, path):
        self.pathvars[var_name].add_path(path)

        self.my_env[var_name] = str(self.pathvars[var_name])

    def dump(self):
        print self.my_env

    def build_path(self):
        """Generate environment path setting from internal path list."""

        self.my_env["PATH"] = ':'.join(self.path_list)


    def add_path(self, path):
        """Add new path to internal path list and rebuild path."""
        self.path_list.insert(0, path)
        self.build_path()

    def run_command(self, command):
        """Run a command with our internal environment."""
        try:
            p = subprocess.Popen(command, env=self.my_env)
        except OSError, e:
            print "OSError", e
            print "Command was ", command
            sys.exit(2)

        p.wait()

        return p.returncode

    def set_variable(self, variable, value):
        self.my_env[variable] = value

    def __getattr__(self, name):

        if name in self.my_env:
            return self.my_env[name]
        
        raise AttributeError('No variable in environment: {}'.format(name))

    def update_CPPFLAGS(self):
        self.my_env['CPPFLAGS'] = ' '.join('-I' + s 
                                           for s in self.CPATH.split(":"))

    def update_LDFLAGS(self):
        self.my_env['LDFLAGS'] = ' '.join('-L' + s 
                                          for s in self.LIBRARY_PATH.split(":"))

def test_env_manager():

    myenv = EnvManager()

    myenv.add_path('/usr/bin')
    myenv.add_path('/bin')

    myenv.dump()

    myenv.run_command('ls')

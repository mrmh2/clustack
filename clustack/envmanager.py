import os
import subprocess

class EnvManager(object):
    """Manage UNIX environment variables for specific building"""

    def __init__(self):
        self.start_env = os.environ.copy()
        self.path_list = self.start_env['PATH'].split(':')
        self.my_env = self.start_env

    def dump(self):
        print self.my_env

    def build_path(self):
        """Generate environment path setting from internal path list"""

        self.my_env["PATH"] = ':'.join(self.path_list)

    def add_path(self, path):
        """Add new path to internal path list and rebuild path"""
        self.path_list.insert(0, path)
        self.build_path()

    def run_command(self, command):
        """Run a command with our internal environment"""
        p = subprocess.Popen(command, env=self.my_env)
        p.wait()

        return p.returncode

    def set_variable(self, variable, value):
        self.my_env[variable] = value

    def __getattr__(self, name):

        if name in self.my_env:
            return self.my_env[name]
        
        raise AttributeError

def test_env_manager():

    myenv = EnvManager()

    myenv.add_path('/usr/bin')
    myenv.add_path('/bin')

    myenv.dump()

    myenv.run_command('ls')

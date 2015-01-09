import os
import subprocess

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

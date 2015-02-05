import os
import sys
import ConfigParser

config = ConfigParser.ConfigParser()

user_config = os.path.expanduser('~/.clustack/settings.cfg')
# Last file in list overrides
read_files = config.read(['config/settings.cfg', user_config])

if not len(read_files):
    print "Error reading setting"
    sys.exit(0)

shelf_dir = config.get('Path settings', 'shelf_dir')

if shelf_dir == "CWD":
    shelf_dir = os.path.join(os.getcwd(), 'shelf')
#shelf_dir = os.path.join(os.getcwd(), 'shelf')

base_program_dir = os.getcwd()

yaml_dir = os.path.join(base_program_dir, 'yaml')
yaml_ext = '.yaml'

stack_dir = os.path.join(base_program_dir, 'stacks')

blueprint_path = [yaml_dir]
blueprint_exts = [yaml_ext]

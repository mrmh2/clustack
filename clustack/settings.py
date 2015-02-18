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

clustack_root = os.environ['CLUSTACK_ROOT']

yaml_dir = os.path.join(clustack_root, 'yaml')
yaml_ext = '.yaml'

stack_dir = os.path.join(clustack_root, 'stacks')

blueprint_path = [yaml_dir]
blueprint_exts = [yaml_ext]

resource_dir = os.path.join(clustack_root, 'resources')
template_dir = os.path.join(resource_dir, 'templates')

module_template = 'module.j2'
module_dir = os.path.join(clustack_root, 'modulefiles')

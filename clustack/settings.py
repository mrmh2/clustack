import os
import ConfigParser

config = ConfigParser.ConfigParser()

user_config = os.path.expanduser('~/.clustack/settings.cfg')
config.read([user_config, 'config/settings.cfg'])

shelf_dir = config.get('Path settings', 'shelf_dir')

if shelf_dir == "CWD":
    shelf_dir = os.path.join(os.getcwd(), 'shelf')
#shelf_dir = os.path.join(os.getcwd(), 'shelf')

yaml_dir = os.path.join(os.getcwd(), 'yaml')
yaml_ext = '.yaml'

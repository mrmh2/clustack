import os
import ConfigParser

config = ConfigParser.ConfigParser()

config.read('config/settings.cfg')

shelf_dir = config.get('Path settings', 'shelf_dir')

if shelf_dir == "CWD":
    shelf_dir = os.path.join(os.getcwd(), 'shelf')
#shelf_dir = os.path.join(os.getcwd(), 'shelf')

yaml_dir = os.path.join(os.getcwd(), 'yaml')
yaml_ext = '.yaml'

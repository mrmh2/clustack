import os
import ConfigParser

config = ConfigParser.ConfigParser()

config.read('config/settings.cfg')

shelf_dir = config.get('Path settings', 'shelf_dir')
#shelf_dir = os.path.join(os.getcwd(), 'shelf')

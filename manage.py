from flask_migrate import Migrate
from os import environ
from sys import exit

from config import config_dict
from app import create_app, db

get_config_mode = environ.get('FLASK_CONFIG_MODE', 'Debug')

config_mode = config_dict.get(get_config_mode, '')
print(config_mode)
if not config_mode:
    raise Exception('Error: Invalid FLASK_CONFIG_MODE environment variable entry.')
app = create_app(config_mode)
Migrate(app, db)

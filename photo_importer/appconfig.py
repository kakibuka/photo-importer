import os
from datetime import datetime

class AppConfig:
    APP_DIR = '~/.photo-importer'
    DATABASE = os.path.join(APP_DIR, 'photo_importer.db')
    TIMEZONE = datetime.now().astimezone().tzinfo # get default timezone
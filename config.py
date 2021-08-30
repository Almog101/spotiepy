from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

class CONFIG:
    DRIVER_PATH = config['PATH'].get('driver_path')
    BINARY_PATH = config['PATH'].get('binary_path')
    HEADLESS = config['DRIVER_OPTIONS'].getboolean('headless')

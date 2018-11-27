import configparser

config = configparser.ConfigParser()
config.read('.env')


def get_value(key):
    return config['DEFAULT'].get(key)


def set_value(key, value):
    config['DEFAULT'][key] = value

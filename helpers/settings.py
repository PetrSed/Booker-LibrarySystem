import configparser


def check_settings():
    return False


def get_settings():
    config = configparser.ConfigParser()
    config.read("config.conf")
    connection_type = config.get("Settings", "connection_type")
    api_server = config.get("Settings", "api_server")
    return connection_type, api_server


def is_first_start():
    return False

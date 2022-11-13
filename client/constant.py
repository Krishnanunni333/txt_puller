import configparser
config = configparser.ConfigParser()
config.read('./store.properties')

PROTOCOL = config.get("endpoint", "protocol")
HOST = config.get("endpoint", "host")
PORT = config.get("endpoint", "port")

URL = PROTOCOL + "://" + HOST + ":" + PORT
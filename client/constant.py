import configparser
config = configparser.ConfigParser()
config.read('store.properties')

PROTOCOL = config.get("endpoint", "protocol")
DOMAIN = config.get("endpoint", "domain")
PORT = config.get("endpoint", "port")

URL = PROTOCOL + "://" + DOMAIN + ":" + PORT
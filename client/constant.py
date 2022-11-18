import configparser
import os


PROPERTIES_PATH = os.getenv('PROPERTIES_PATH') +  '/store.properties'
print(f"The properties values are fetched from this file: {PROPERTIES_PATH}")


config = configparser.ConfigParser()
config.read(PROPERTIES_PATH)

PROTOCOL = config.get("endpoint", "protocol")
HOST = config.get("endpoint", "host")
PORT = config.get("endpoint", "port")

URL = PROTOCOL + "://" + HOST + ":" + PORT
import configparser
config = configparser.ConfigParser()
config.read('app.properties')

TXT_PATH = config.get("folder", "txt_folder_path")
META_PATH = config.get("folder", "metadata_folder_path")
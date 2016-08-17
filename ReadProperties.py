import configparser

class ConfigParser():

    def read_config(self):
        config = configparser.ConfigParser()
        config.read('properties')

        return config
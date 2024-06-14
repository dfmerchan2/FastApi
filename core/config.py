"""Module to store environment configs"""

import os


class Config(object):
    """Parent class for environment configs"""

    ENV = os.environ.get("ENV", "DEVELOPMENT")
    MODE_TEST = os.environ.get("MODE_TEST", 'DEVELOP').lower()
    HOST = os.environ.get("HOST", "localhost:")
    PORT = os.environ.get("PORT", "5001")
    SECRET_KEY = os.environ.get("SECRET_KEY", "this_is_a_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG: bool = False
    SQLALCHEMY_DATABASE_URI: str = ""

    def get_environment_config(self, ENV) -> str:
        """To supports several environments"""
        if ENV == "TESTING":
            self.DEBUG = False
            self.SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"  # will be searching for test.db file in instance folder, if does not exist, will create new one
            return self.SQLALCHEMY_DATABASE_URI
        elif ENV == "DEVELOPMENT":
            self.DEBUG = True
            self.SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"  # will be searching for dev.db file in instance folder, if does not exist, will create new one
            return self.SQLALCHEMY_DATABASE_URI

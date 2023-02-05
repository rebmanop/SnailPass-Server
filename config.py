import os
import tempfile

class Config(object):
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.environ['SNAILPASS_SECRET_KEY']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    @property
    def SQLALCHEMY_DATABASE_URI(self):  
        self.db_fd, self.db_filename = tempfile.mkstemp(suffix='.sqlite')
        return f"sqlite:///{self.db_filename}"


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///../devdatabase.db"
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SNAILPASS_DATABASE_URI")
    DEBUG = False

config = {"testing": TestingConfig, "dev": DevelopmentConfig, "prod": ProductionConfig}
import os
import tempfile

class Config(object):
    TESTING = False
    DEBUG = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SECRET_KEY = os.environ['SNAILPASS_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ["SNAILPASS_DB_URI"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


class TestingConfig(Config):
    SECRET_KEY = os.environ['SNAILPASS_SECRET_KEY']
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    TESTING = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):  
        self.db_fd, self.db_filename = tempfile.mkstemp(suffix='.sqlite')
        return f"sqlite:///{self.db_filename}"
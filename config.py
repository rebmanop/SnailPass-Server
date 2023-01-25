import os
import tempfile


class Config(object):
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.environ['SNAILPASS_SECRET_KEY']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ["SNAILPASS_DB_URI"]
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    @property
    def SQLALCHEMY_DATABASE_URI(self):  
        self.db_fd, self.db_filename = tempfile.mkstemp(suffix='.sqlite')
        return f"sqlite:///{self.db_filename}"
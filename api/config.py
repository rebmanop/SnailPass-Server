import os
import tempfile


class Config(object):
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.environ.get("SNAILPASS_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BUNDLE_ERRORS = True
    PROPAGATE_EXCEPTIONS = True


class TestingConfig(Config):
    SECRET_KEY = "testing_env_secret_key"
    TESTING = True
    DEBUG = True

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        self.db_fd, self.db_filename = tempfile.mkstemp(suffix=".sqlite")
        return f"sqlite:///{self.db_filename}"


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///../devdatabase.db"
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SNAILPASS_DATABASE_URI")
    DEBUG = False

    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")


config = {"testing": TestingConfig, "dev": DevelopmentConfig, "prod": ProductionConfig}

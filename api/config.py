from datetime import timedelta
import os
from decouple import config

basedir = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATION = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "student.db")
    DEBUG = True  


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"  # for in-memory database
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):    
    # uri = config("DATABASE_URL")
    # if uri.startswith("postgres://"):
    #     uri = uri.replace("postgres://", "postgresql://", 1)

    # SQLALCHEMY_DATABASE_URI = uri
    # DEBUG = config("DEBUG", False, cast=bool)
    # SQLALCHEMY_ECHO = False

    pass

config_dict = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

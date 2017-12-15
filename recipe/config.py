#instance/config.py
import os
#from sqlalchemy import SQLALCHEMY_DATABASE_URI
# from sqlalchemy.orm import scoped_session, sessionmaker

# SQLALCHEMY_DATABASE_URI = ""

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = 'xcEN1Sbcp39XKraZVytFEzDJdKVDZZRg'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #global SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:phiona@localhost:5432/recipe_api'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    # global SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:phiona@localhost:5432/test_db'
    DEBUG = True

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

# Session = sessionmaker()
#engine = create_engine(SQLALCHEMY_DATABASE_URI)
# Session.configure(bind=engine)

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
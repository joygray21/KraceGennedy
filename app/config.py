import os

class Config(object):
    """Base Config Object"""
    DEBUG = False

    # Key for OpenWeather API
    API_KEY = os.environ.get("API_KEY")

    # Company preferences
    UNITS = 'metric' #unit of measure that should be used for forecast values
    RAINY_DAY_DEF = 50  #a day with 50mm or more of rain is considered a rainy day
    BOSS_EMAIL = 'boss@kracegennedy.org'
    BOSS_NAME = 'Kennedy Graham'
    
    #SECRET_KEY = os.environ.get('SECRET_KEY') or 'Som3$ec5etK*y'

    # Database 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://yourusername:yourpassword@localhost/databasename'
    SQLALCHEMY_TRACK_MODIFICATIONS = False # This is just here to suppress a warning from SQLAlchemy as it will soon be removed

    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = os.environ.get('MAIL_PORT') or '25'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    

class DevelopmentConfig(Config):
    """Development Config that extends the Base Config Object"""
    DEVELOPMENT = True
    DEBUG = True

class ProductionConfig(Config):
    """Production Config that extends the Base Config Object"""
    DEBUG = False
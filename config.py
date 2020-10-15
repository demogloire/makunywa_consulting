class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments
    DEBUG = True

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    SECRET_KEY = '9462bfc3ca8d37b136173798873d05ea'
    DEBUG = True
    SQLALCHEMY_ECHO = True
    MAIL_SERVER = 'mail.humanitaire.cd'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "noreply@humanitaire.cd"
    MAIL_PASSWORD = "Standup@2020"
    account_sid = 'AC6ae3e81d9f78448d62d93da0f6ebad34'
    auth_token = '21aedb0020969d30b4e7d16629fd3c4d'



class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    SECRET_KEY = '9462bfc3ca8d37b136173798873d05ea'
    DEBUG = True
    SIMPLEMDE_JS_IIFE = False
    SIMPLEMDE_USE_CDN = False
    MAIL_SERVER = 'mail.humanitaire.cd'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = "noreply@humanitaire.cd"
    MAIL_PASSWORD = "Standup@2020"
    account_sid = 'AC6ae3e81d9f78448d62d93da0f6ebad34'
    auth_token = '21aedb0020969d30b4e7d16629fd3c4d'
class TestingConfig(Config):
    """
    Testing configurations
    """

    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

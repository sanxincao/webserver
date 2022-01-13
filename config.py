import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    #MAIL_PORT = int(os.environ.get('MAIL_PORT')) or '465'
    MAIL_PORT = 465
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
    #     ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'lonelyparabola@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'ztc1639643261'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'lonelyparabola@gmail.com'
    #FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'lonelyparabola@gmail.com'
    MAIL_USE_TLS=False
    MAIL_USE_SSL=True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #TODO 提醒用户将链接贴到浏览器上，防止503跳转失败
    @staticmethod
    def init_app(app):
        pass
#ppepbfevrrqmbibb
#hhixrhhzaekwdejc

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    #SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:password@localhost:3306/webserver'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

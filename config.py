import os
basedir=os.path.abspath(__file__)

class Config:
  SECRET_KEY=os.environ.get('SECRET_KEY') or 'hard string'
  SQLALCHEMY_COMMOT_OM_TEARDOWN=True
  #todo the email sender config
  @staticmethod
  def init_app(app):
    pass

class DevcConfig(Config):
  DEBUG=True
  #todo the email sender config
  SQLALCHEMY_DATABASE_URI=''
class Production(Config):
  DEBUG=True
  #todo the email sender config
  SQLALCHEMY_DATABASE_URI=''
config={
  'devconfig':DevcConfig,
  'production':Production,
  'default':DevcConfig
}
import os

class BaseConfig(object):
   PROJECT = "app" 
   
   # Get app root path, also can use flask.root_path.
   PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
   
   DEBUG = False
   USE_EMAIL = True
   TESTING = False
   PROD      = False
   
   ADMINS = ['youremail@yourdomain.com']
   
   #for session
   SECRET_KEY = 'RANDOM_SECRET_KEY'
   API_ROOT = 'api'
   
class DefaultConfig(BaseConfig):
   SITE_NAME = "GateControl"
   # Enable protection agains *Cross-site Request Forgery (CSRF)*
   WTF_CSRF_ENABLED = True
   
class LocalConfig(DefaultConfig):
   DEBUG = True
   USE_EMAIL = False
   DOMAIN_NAME = 'localhost:5000'
   SQLALCHEMY_ECHO = False
   PROD      = False
   
   
class TestConfig(BaseConfig):
   #Set Testing to False so we still have authentication when unit testing
   WTF_CSRF_ENABLED = False
   DOMAIN_NAME = 'localhost:5000'
   TESTING = False
   
class StagingConfig(DefaultConfig):
   DOMAIN_NAME = 'STAGING_DOMAIN'
   DEBUG = False
   USE_EMAIL = False
   PROD      = True
   
class ProdConfig(DefaultConfig):
   DOMAIN_NAME = 'raspberrypi.local'
   DEBUG = False
   USE_EMAIL = True
   PROD      = True
   
def get_config(MODE):
   SWITCH = {
      'LOCAL'     : LocalConfig,
      'STAGING'   : StagingConfig,
      'PRODUCTION': ProdConfig
   }
   return SWITCH[MODE]
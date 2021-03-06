import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

dotenv_path = os.path.join(basedir, '.env')
load_dotenv(dotenv_path)


class Config:
    # falsk的内置config key: https://flask.palletsprojects.com/en/2.0.x/config/
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(16)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL') or 'no found DEV_DATABASE_URL on .env'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    PRODUCTION_CONFIG = False

    # 公众号配置
    WEROBOT_ID = os.environ.get(
        'WEROBOT_ID') or 'no found WEROBOT_ID on .env'
    WEROBOT_SECRET = os.environ.get(
        'WEROBOT_SECRET') or 'no found WEROBOT_SECRET on .env'

    # 阿里ocr api
    OCR_APP_ID = os.environ.get(
        'OCR_APP_ID') or 'no found OCR_APP_ID on .env'
    OCR_API_KEY = os.environ.get(
        'OCR_API_KEY') or 'no found OCR_API_KEY on .env'
    OCR_SECRET_KEY = os.environ.get(
        'OCR_SECRET_KEY') or 'no found OCR_SECRET_KEY on .env'

    # init_app是为了在初始化app时附加一些额外配置用的

    @ classmethod
    def init_app(cls, app):

        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = True
    PRODUCTION_CONFIG = False


class ProductionConfig(Config):
    SQLALCHEMY_ECHO = False
    PRODUCTION_CONFIG = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

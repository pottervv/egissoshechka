import os

class Config(object):
    # Определяет, включен ли режим отладки
    # В случае если включен, flask будет показывать
    # подробную отладочную информацию. Если выключен -
    # - 500 ошибку без какой либо дополнительной информации.
    DEBUG = False
    # Включение защиты против "Cross-site Request Forgery (CSRF)"
    CSRF_ENABLED = True
    # Случайный ключ, которые будет исползоваться для подписи
    # данных, например cookies.
    SECRET_KEY = 'YOUR_RANDOM_SECRET_KEY'
    # URI используемая для подключения к базе данных
    #SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    PATH=path=os.path.abspath(os.path.dirname(__file__))


class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class ViberBotConfig(Config):
    name = 'helpegisso',
    avatar = 'http://viber.com/avatar.jpg',
    auth_token = '496bdc821627d6e3-89019a2a752a3f08-58f225f6ba43594'


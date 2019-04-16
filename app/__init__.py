"""
__init__.py
Создание  объекта приложения как экземпляра Flask,
импортированного из пакета flask
"""
from flask import Flask, request, Response, jsonify,json
from ..config import *
from viberbot import Api

from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages.keyboard_message import KeyboardMessage


from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest


import time
import logging
import sched
import threading

"""
Переменная webApp определяется как экземпляр класса Flask в сценарии __init__.py, 
что делает его частью пакета приложения.
"""
app = Flask(__name__)
app.config.from_object(Config)

viber = Api(BotConfiguration(
    name=ViberBotConfig().name,
    avatar=ViberBotConfig().avatar,
    auth_token=ViberBotConfig().auth_token
))


def set_webhook(viber):
    viber.set_webhook('https://egissoshechka.herokuapp.com:443')
    logging.info("Web hook has been set")
#webApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#webApp.config['SECRET_KEY'] = "random string"

"""
Импорт модуля представлений
view — это разные URL-адреса, которые приложение реализует. 
"""
from egissoshechka.app import view
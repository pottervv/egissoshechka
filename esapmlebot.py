# -*- coding: utf-8 -*-
import sqlite3
import json
import keyboards
from answers import answers

from flask import Flask, request, Response, send_from_directory
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
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

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

token = "4723336bb367d06e-ab321ee6503a0206-58d9d2bfcc9b6386"

avatar = 'https://pbs.twimg.com/profile_images/378800000472528007/7e3d601acd34222cd0e1accff4b92d2a_400x400.jpeg'
# test_token='47180bc4e627d501-2fd700adf2113640-bb3e6b0f5459b969'

app = Flask(__name__)
viber = Api(BotConfiguration(
    name='ГрузоБот',
    avatar=avatar,
    auth_token=token
))

conn = sqlite3.connect('database.db')
c = conn.cursor()


# ['id','stage','vehicle','time','place','loaders'] varchar

def get_reply(stage, text, user_id):
    # по дефолту ответом является сообщение клиента, клавиатуры - нет
    reply = "Я тебя не понял!🚚\nStage:{}".format(stage)
    keyboard = None

    if stage == "1":
        c.execute("UPDATE users SET vehicle = '', extra='', loaders='', place='', time='' WHERE id = '%s';" % user_id)
        conn.commit()
        try:
            reply = answers["1"][text]
        except:
            pass
        keyboard = keyboards.first

        if text == "Начать!":
            c.execute("UPDATE users SET stage = '2' WHERE id = '%s';" % user_id)
            conn.commit()
            keyboard = keyboards.second

    elif stage == '2':
        # ВЫБОР МАШИНЫ
        keyboard = keyboards.second
        if reply == "Отменить заявку":
            c.execute("UPDATE users SET stage = '1' WHERE id = '%s';" % user_id)
            conn.commit()
            reply = "Ваша заявка отменена!😃"
            keyboard = keyboards.first
        else:
            # Выбран один из вариантов машины
            c.execute("UPDATE users SET stage = '3', vehicle = '%s' WHERE id = '%s';" % (text, user_id))
            conn.commit()
            keyboard = keyboards.third
            reply = answers['2']

    elif stage == '3':
        # Пользователь отправил место
        if text == "Отменить заявку":
            # отмена заявки
            c.execute("UPDATE users SET stage = '1' WHERE id = '%s';" % user_id)
            conn.commit()
            reply = "Ваша заявка отменена!😃"
            keyboard = keyboards.first
        elif text == "Исправить заявку":
            # Исправление заявки
            c.execute("UPDATE users SET stage = 'correction' WHERE id = '%s';" % user_id)
            conn.commit()
            reply = answers['correction']
            keyboard = keyboards.correction

        else:
            # Если отправлено место (в том числе локация, НУЖНО ДОДЕЛАТЬ)
            text = str(text)
            c.execute("UPDATE users SET stage = '4', place = '%s' WHERE id = '%s';" % (text, user_id))
            conn.commit()
            reply = answers['3']
            keyboard = keyboards.fourth

    elif stage == '4':
        # Пользователь отправил время
        if text == "Отменить заявку":
            # отмена заявки
            c.execute("UPDATE users SET stage = '1' WHERE id = '%s';" % user_id)
            conn.commit()
            reply = "Ваша заявка отменена!😃"
            keyboard = keyboards.first
        elif text == "Исправить заявку":
            # Исправление заявки
            c.execute("UPDATE users SET stage = 'correction' WHERE id = '%s';" % user_id)
            conn.commit()
            reply = answers['correction']
            keyboard = keyboards.correction

        else:
            # Если отправлено время
            c.execute("UPDATE users SET stage = '5', time = '%s' WHERE id = '%s';" % (text, user_id))
            conn.commit()
            reply = answers['4']
            c.execute("SELECT vehicle,place,time,loaders,extra FROM users WHERE id = '%s'" % user_id)
            vehicle, place, time, loaders, extra = c.fetchall()[0]
            if loaders == "":
                loaders = "Нет"
            if extra == "":
                extra = "Нет"
            reply = reply % (vehicle, place, time, loaders, extra)
            keyboard = keyboards.fifth

    elif stage == '5':
        keyboard = keyboards.fifth
        if text == "Отменить заявку":
            # отмена заявки
            c.execute("UPDATE users SET stage = '1' WHERE id = '%s';" % user_id)
            conn.commit()
            reply = "Ваша заявка отменена!😃"
            keyboard = keyboards.first
        elif text == "Исправить заявку":
            # Исправление заявки
            c.execute("UPDATE users SET stage = 'correction' WHERE id = '%s';" % user_id)
            conn.commit()
            reply = answers['correction']
            keyboard = keyboards.correction
        elif text == "Подтвердить заявку":
            keyboard = keyboards.first
            reply = answers["end"]
            c.execute("SELECT vehicle,place,time,loaders,extra FROM users WHERE id = '%s'" % user_id)
            reply += "\n" + str(c.fetchall()[0])
            c.execute("UPDATE users SET stage = '1' WHERE id = '%s';" % user_id)
            conn.commit()
        elif text == "Особые пожелания":
            c.execute("UPDATE users SET stage = '7' WHERE id = '%s';" % user_id)
            conn.commit()
            reply = answers["7"]
            keyboard = None
        elif text == "Нанять грузчиков":
            c.execute("UPDATE users SET stage = '6' WHERE id = '%s';" % user_id)
            conn.commit()
            reply = answers['6']
            keyboard = keyboards.sixth

    elif stage == '6':
        # Грузчики
        if text == "Отменить заявку":
            # отмена заявки
            c.execute("UPDATE users SET stage = '1' WHERE id = '%s';" % user_id)
            conn.commit()
            reply = "Ваша заявка отменена!😃"
            keyboard = keyboards.first
        elif text == "Исправить заявку":
            # Исправление заявки
            c.execute("UPDATE users SET stage = 'correction' WHERE id = '%s';" % user_id)
            conn.commit()
            reply = answers['correction']
            keyboard = keyboards.correction
        else:
            # выбрано что-то в качестве варианта
            c.execute("UPDATE users SET loaders = '%s', stage='5' WHERE id = '%s';" % (text, user_id))
            conn.commit()
            c.execute("SELECT vehicle,place,time,loaders,extra FROM users WHERE id = '%s'" % user_id)
            vehicle, place, time, loaders, extra = c.fetchall()[0]
            reply = answers['4']
            if loaders == "":
                loaders = "Нет"
            if extra == "":
                extra = "Нет"
            reply = reply % (vehicle, place, time, loaders, extra)
            keyboard = keyboards.fifth


    elif stage == '7':
        # Особые пожелания
        if text == "Отменить заявку":
            # отмена заявки
            c.execute("UPDATE users SET stage = '1' WHERE id = '%s';" % user_id)
            conn.commit()
            reply = "Ваша заявка отменена!😃"
            keyboard = keyboards.first
        elif text == "Исправить заявку":
            # Исправление заявки
            c.execute("UPDATE users SET stage = 'correction' WHERE id = '%s';" % user_id)
            conn.commit()
            reply = answers['correction']
            keyboard = keyboards.correction
        else:
            # выбрано что-то в качестве варианта
            c.execute("UPDATE users SET extra = '%s', stage='5' WHERE id = '%s';" % (text, user_id))
            conn.commit()
            c.execute("SELECT vehicle,place,time,loaders,extra FROM users WHERE id = '%s'" % user_id)
            vehicle, place, time, loaders, extra = c.fetchall()[0]
            reply = answers['4']
            if loaders == "":
                loaders = "Нет"
            if extra == "":
                extra = "Нет"
            reply = reply % (vehicle, place, time, loaders, extra)
            keyboard = keyboards.fifth
    elif stage == 'correction':
        if text == 'Выбор автомобиля':
            c.execute("UPDATE users SET stage='2' WHERE id = '%s';" % (user_id))
            conn.commit()
            keyboard = keyboards.second
            reply = answers["1"]["Начать!"]
        elif text == "Выбор места":
            c.execute("UPDATE users SET stage='3' WHERE id = '%s';" % (user_id))
            conn.commit()
            keyboard = keyboards.third
            reply = answers["2"]
        elif text == "Время подачи":
            c.execute("UPDATE users SET stage='4' WHERE id = '%s';" % (user_id))
            conn.commit()
            keyboard = keyboards.fourth
            reply = answers["3"]
        elif text == "Особые пожелания":
            c.execute("UPDATE users SET stage='7' WHERE id = '%s';" % (user_id))
            conn.commit()
            keyboard = None
            reply = answers["7"]
        elif text == "Грузчики":
            c.execute("UPDATE users SET stage='6' WHERE id = '%s';" % (user_id))
            conn.commit()
            keyboard = None
            reply = answers["6"]

    return reply, keyboard


@app.route('/images/<path:path>')
def send_js(path):
    return send_from_directory('images', path)


@app.route('/', methods=['POST'])
def incoming():
    logger.debug("received request. post data: {0}".format(request.get_data()))

    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        # ОТВЕТ НА СООБЩЕНИЕ ЮЗЕРА

        user_id = str(viber_request.sender.id)
        message = ""

        try:
            message = viber_request.message.text
        except:
            try:
                message = str(viber_request.message.location)
            except:
                pass

        c.execute("SELECT stage FROM users WHERE id= '%s';" % user_id)
        stage = c.fetchall()

        #        viber.send_messages(viber_request.sender.id, [
        #                    TextMessage(text=str(stage),keyboard=keyboards.first)
        #                ])

        if stage != []:
            stage = stage[0][0]
        else:
            # Если что-то пошло не так(мало ли, ребутнется сервер), начинаем с этапа 1
            stage = 1
            c.execute("UPDATE users SET stage = '1' WHERE id = '%s';" % user_id)
            conn.commit()

        text, keyboard = get_reply(stage, message, user_id)
        viber.send_messages(viber_request.sender.id, [
            TextMessage(text=text, keyboard=keyboard)
        ])


    elif isinstance(viber_request, ViberConversationStartedRequest):
        # ОТВЕТ НА НАЧАЛО ОБЩЕНИЯ С БОТОМ
        reply = """Здравствуйте🖖!
Меня зовут GruzBot🤖.Я помогу вам:
   - вызвать грузовое такси за три простых шага🚚.
   - нанять грузчиков💪."""
        c.execute("INSERT INTO users(id,stage) VALUES ('%s', '1')" % (str(viber_request.user.id)))
        conn.commit()

        viber.send_messages(viber_request.user.id, [
            TextMessage(text=reply, keyboard=keyboards.first)
        ])

    elif isinstance(viber_request, ViberFailedRequest):
        logger.warn("client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)


def set_webhook():
    while True:
        old_url = 'https://viberrooot.herokuapp.com/'
        url = "https://gruzobot.herokuapp.com/"
        viber.set_webhook(url)
        time.sleep(3600)


if __name__ == "__main__":
    viber.set_webhook("https://gruzobot.herokuapp.com/")
    t = threading.Thread(target=set_webhook)
    t.start()
    app.run(debug=True)
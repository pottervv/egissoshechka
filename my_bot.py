from flask import Flask, request, Response,Request,jsonify
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages.sticker_message import StickerMessage
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
import json


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)
viber = Api(BotConfiguration(
    name='helpegisso',
    avatar='http://egisso.ru/site/img/family.efd5d97b4a8a3b65d467d2ad40303706.png',
    auth_token='496bdc821627d6e3-89019a2a752a3f08-58f225f6ba43594'
))


def set_webhook(viber):
    viber.set_webhook('https://egissoshechka.herokuapp.com:443')
    logger.info("Web hook has been set")

@app.route('/', methods=['POST'])
def incoming():
    keyboarddate ="""{
        "DefaultHeight": True,
        "BgColor": "#FFFFFF",
        "Buttons": [{
            "Columns": 6,
            "Rows": 1,
            "BgColor": "#2db9b9",
            "BgMediaType": "gif",
            "BgLoop": True,
            "ActionType": "open-url",
            "ActionBody": "www.tut.by",
            "Text": "Key text",
            "TextVAlign": "middle",
            "TextHAlign": "center",
            "TextOpacity": 60,
            "TextSize": "regular"
        }]
    }"""
    diser = jsonify(keyboarddate)
    keyboard=json.dumps(keyboarddate)
    keyb={"DefaultHeight": True}

    logger.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method

    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberConversationStartedRequest):
        viber.send_messages(viber_request.user.id, [TextMessage(text="Здравствуйте! Вас приветствует бот helpegisso.")])
        logger.debug(" viber_request.get_user().get_id()-{0}".format(viber_request.user.id))
        logger.debug("keyboard:{0}".format(keyboard))
    if isinstance(viber_request, ViberSubscribedRequest):
             viber.send_messages(viber_request.user,[TextMessage(text="Спасибо за подписку!")])
             logger.debug("_viber_request.get_event_type():{0}".format(viber_request.get_event_type()))

    elif isinstance(viber_request, ViberUnsubscribedRequest):
        #viber.send_messages(viber_request.user_id, viber_request.get_event_type())
        viber.send_messages(viber_request.user_id, [TextMessage(text="Вы отписались!")])
        logger.debug("1_viber_request.get_event_type():{0}".format(viber_request.get_event_type()))

    elif isinstance(viber_request, ViberFailedRequest):
        logger.warning("client failed receiving message. failure: {0}".format(viber_request))


    if isinstance(viber_request, ViberMessageRequest):
        messages_echo = viber_request.message
        logger.debug("keyboard:{0}".format(keyboard))
        #viber.send_messages(to=viber_request.sender.id, messages=[messages])
        #if messages=="0":
        message_stiker = StickerMessage(sticker_id=40100);
        message_key = KeyboardMessage(tracking_data=json.dumps({"text":"purga"}), keyboard=keyboard)
        logger.debug("keyboard:{0}".format(keyboard))
        text_m=TextMessage(text="Для начинающих")
        account_info = TextMessage(text=str(viber_request.sender.name))
        #viber.send_messages(to=viber_request.sender.id, messages=[text_m])
        viber.post_messages_to_public_account(sender=viber_request.get_sender().get_id(),
                                                       messages=[TextMessage(text="sample message")])

    return Response(status=200)




if __name__ == "__main__":


    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(5, 1, set_webhook, (viber,))
    t = threading.Thread(target=scheduler.run)
    t.start()

    context = ('ssl/viber.crt', 'ssl/viber.key')
    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=context)




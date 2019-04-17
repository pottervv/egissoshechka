from flask import Flask, request, Response, jsonify,json
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
import json
import simplejson as s_json

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)
viber = Api(BotConfiguration(
    name='helpegisso',
    avatar='http://viber.com/avatar.jpg',
    auth_token='496bdc821627d6e3-89019a2a752a3f08-58f225f6ba43594'
))


def set_webhook(viber):
    viber.set_webhook('https://egissoshechka.herokuapp.com:443')
    logging.info("Web hook has been set")

'''
viber_request = viber.parse_request(request.get_data())
logging.info("Web hook has been set")
print(viber_request)
'''
def get_json():
    s={
   "receiver":"01234567890A=",
   "type":"text",
   "text":"Hello world",
   "keyboard":{
      "Type":"keyboard",
      "DefaultHeight":True,
      "Buttons":[
         {
            "ActionType":"reply",
            "ActionBody":"reply to me",
            "Text":"Key text",
            "TextSize":"regular"
         }
         ]
         }
         }
    return s


@app.route('/', methods=['POST'])
def incoming():

    keyboard={
            "type":"keyboard",
            "DefaultHeight": True,
            "InputFieldState":"hidden",
            "BgColor": "#FFFFFF",
            "Buttons": [{
                "Columns": 6,
                "Rows": 1,
                "BgColor": "#2db9b9",
                "BgMediaType": "gif",
                "BgMedia": "http://www.url.by/test.gif",
                "BgLoop": True,
                "ActionType": "open-url",
                "ActionBody": "www.tut.by",
                "Image": "www.tut.by/img.jpg",
                "Text": "Key text",
                "TextVAlign": "middle",
                "TextHAlign": "center",
                "TextOpacity": 60,
                "TextSize": "regular"
            }]
        }



    tracking_data =  """{
                "type": "text",
                "text": "Welcome to our bot!"
                 }"""




    logger.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberConversationStartedRequest):
        viber.send_messages(viber_request.get_user().get_id(), [ TextMessage(text="Welcome!")])
        logger.debug(" viber_request.get_user().get_id()-{0}".format(viber_request.get_user().get_id()))

    elif isinstance(viber_request, ViberMessageRequest):
       viber.send_messages(to=viber_request.sender.id,messages=[TextMessage(text="sample message")])


    elif isinstance(viber_request, ViberSubscribedRequest):
             #viber.send_messages(viber_request.sender.id, [TextMessage(viber_request.get_event_type())])
             viber.send_messages(viber_request.get_user().get_id(),
                                 [TextMessage(text="Здравствуйте! Вас приветствует бот helpegisso. Все о мире ЕГИССО")])

             logger.debug("viber_request.get_event_type():{0}".format(viber_request.get_event_type()))

    elif isinstance(viber_request, ViberUnsubscribedRequest):
        viber.send_messages(viber_request.get_user().get_id(), [TextMessage(text="Вы отписались!")])


    elif isinstance(viber_request, ViberFailedRequest):
        logger.warning("client failed receiving message. failure: {0}".format(viber_request))


    return Response(status=200)




if __name__ == "__main__":

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(5, 1, set_webhook, (viber,))
    t = threading.Thread(target=scheduler.run)
    t.start()

    context = ('ssl/viber.crt', 'ssl/viber.key')
    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=context)




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

    tracking_data=jsonify(tracking_data=tracking_data)


    logging.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())
    #viber_request=viber.parse_request(request)


    if isinstance(viber_request, ViberMessageRequest):
        #message = viber_request.message
        #message = TextMessage(text="hello")
        #viber.send_messages(viber_request.sender.id,[message])
        #viber.post_messages_to_public_account(viber_request.sender,[message])
        #viber.send_messages(viber_request.sender.id,[viber.get_account_info()])
        #message= KeyboardMessage(tracking_data=tracking_data ,keyboard=keyboard) #TextMessage(text="my text message")
        viber.send_messages(to=viber_request.sender.id,
                            messages=[TextMessage(text="sample message")])
         # lets echo back
        #viber.send_messages(viber_request.sender.id, [message])


        ''' message = TextMessage(text="hello") #viber_request.message

        # lets echo back
        viber.send_messages(viber_request.sender.id, [
            message
        ])
        '''

    elif     isinstance(viber_request, ViberSubscribedRequest) \
             or isinstance(viber_request, ViberUnsubscribedRequest):
             #viber.send_messages(viber_request.sender.id, [ TextMessage(None, None, viber_request.get_event_type())])
             viber.send_messages(viber_request.user_id, [TextMessage(text="Здравствуйте! Вас приветствует ботhelpegisso. Все о мире ЕГИССО")])
    elif isinstance(viber_request, ViberFailedRequest):
        logging.warning("client failed receiving message. failure: {0}".format(viber_request))


    return Response(status=200)




if __name__ == "__main__":

    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(5, 1, set_webhook, (viber,))
    t = threading.Thread(target=scheduler.run)
    t.start()

    context = ('ssl/viber.crt', 'ssl/viber.key')
    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=context)




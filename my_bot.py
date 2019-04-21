from flask import Flask, request, Response, jsonify
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
#import keyboards
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

keyboardDict ={
    "type": "link",
    "url": "https://en.wikipedia.org/wiki/Viber",
    "title": "Interesting article about Viber",
    "thumbnail": "https://www.viber.com/app/uploads/icon-purple.png",
    "domain": "www.wikipedia.org",
    "width": 480,
    "height": 320,
    "minApiVersion": 4,
    "alternativeUrl": "https://www.egisso.ru",
    "alternativeText": "О боте helpegisso"
}


def set_webhook(viber):
    viber.set_webhook('https://egissoshechka.herokuapp.com:443')
    logging.info("Web hook has been set")

@app.route('/', methods=['POST'])
def incoming():

    #keyboard=json.dumps(keyboard)

    """ 
    tracking_data =  {
                "type": "text",
                "text": "Welcome to our bot!"
                 }
    """



    logger.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberConversationStartedRequest):
        viber.send_messages(viber_request.user.id, [TextMessage(text="Здравствуйте! Вас приветствует бот helpegisso. Все о мире ЕГИССО")])
        logger.debug(" viber_request.get_user().get_id()-{0}".format(viber_request.user.id))

    if isinstance(viber_request, ViberSubscribedRequest):
             #viber.send_messages(viber_request.user.id, viber_request.get_event_type())
             viber.send_messages(viber_request.user,[TextMessage(text="Спасибо за подписку!")])
             logger.debug("_viber_request.get_event_type():{0}".format(viber_request.get_event_type()))

    elif isinstance(viber_request, ViberUnsubscribedRequest):
        #viber.send_messages(viber_request.user_id, viber_request.get_event_type())
        viber.send_messages(viber_request.user_id, [TextMessage(text="Вы отписались!")])
        logger.debug("1_viber_request.get_event_type():{0}".format(viber_request.get_event_type()))

    elif isinstance(viber_request, ViberFailedRequest):
        logger.warning("client failed receiving message. failure: {0}".format(viber_request))


    if isinstance(viber_request, ViberMessageRequest):





       keyboard = json.dumps(keyboardDict)
       viber.send_messages(to=viber_request.sender.id,
                           messages=[TextMessage(keyboard="""{Type:keyboard,
      DefaultHeight:True,
      'Buttons':[
         {
            'ActionType':'reply',
            'ActionBody':'reply to me',
            'Text':'Key text'

         }
      ]}""", text="C Вами так интересно", )])


    return Response(status=200)




if __name__ == "__main__":


    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(5, 1, set_webhook, (viber,))
    t = threading.Thread(target=scheduler.run)
    t.start()

    context = ('ssl/viber.crt', 'ssl/viber.key')
    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=context)




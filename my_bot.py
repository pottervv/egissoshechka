from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage


from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest


import time
import logging
import sched
import threading

app = Flask(__name__)
viber = Api(BotConfiguration(
    name='helpegisso',
    avatar='http://viber.com/avatar.jpg',
    auth_token='496bdc821627d6e3-89019a2a752a3f08-58f225f6ba43594'
))

def set_webhook(viber):
    viber.set_webhook('https://egissoshechka.herokuapp.com:443/viber')

'''
viber_request = viber.parse_request(request.get_data())
logging.info("Web hook has been set")
print(viber_request)
'''

@app.route('/viber', methods=['POST'])
def incoming():
    logging.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        #message = viber_request.message
        message=TextMessage(text="my text message")
        # lets echo back
        viber.send_messages(viber_request.sender.id, [
            message
        ])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="thanks for subscribing!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logging.warning("client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)


@app.route('/incoming', methods=['POST'])
def incoming_():

	logging.debug("received request. post data: {0}".format(request.get_data()))
	# handle the request here
	return Response(status=200)



@app.route('/')
def index():
    return ''' 
    <html>
    <body>
    hello world, test viber_bot
    </body>
    </html>
    '''
""" 
context = ('ssl/viber.crt', 'ssl/viber.key')
app.run(host='0.0.0.0', port=443, debug=True, ssl_context=context)

"""
if __name__ == "__main__":
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(5, 1, set_webhook, (viber,))
    t = threading.Thread(target=scheduler.run)
    t.start()

    context = ('ssl/viber.crt', 'ssl/viber.key')
    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=context)




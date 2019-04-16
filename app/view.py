from ..app import request, Response, jsonify, json, app
from ..app import Api
from ..app import viber
from ..app import TextMessage
from ..app import VideoMessage
from ..app import logging
from ..app import ViberConversationStartedRequest

from ..app import ViberFailedRequest
from ..app import ViberMessageRequest
from ..app import ViberSubscribedRequest
from ..app import ViberUnsubscribedRequest
@app.route('/', methods=['POST'])
def incoming():

    keyboard= """{
            "DefaultHeight": 'true',
            "BgColor": "#FFFFFF",
            "Buttons": [{
                "Columns": 6,
                "Rows": 1,
                "BgColor": "#2db9b9",
                "BgMediaType": "gif",
                "BgMedia": "http://www.url.by/test.gif",
                "BgLoop": 'true',
                "ActionType": "open-url",
                "ActionBody": "www.tut.by",
                "Image": "www.tut.by/img.jpg",
                "Text": "Key text",
                "TextVAlign": "middle",
                "TextHAlign": "center",
                "TextOpacity": 60,
                "TextSize": "regular"
            }]
        }"""

    keyboard=jsonify(keyboard=keyboard)


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

    if isinstance(viber_request, ViberConversationStartedRequest):
        viber.send_messages(viber_request.get_user().get_id(), [
            TextMessage(text="Welcome!")
        ])
    """
    if isinstance(viber_request, ViberMessageRequest):
        #message = viber_request.message
        message= KeyboardMessage(tracking_data=tracking_data ,keyboard=keyboard) #TextMessage(text="my text message")

        # lets echo back
        viber.send_messages(viber_request.sender.id, [
            message
        ])
    """
    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message

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

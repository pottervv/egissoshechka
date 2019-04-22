import json
import hmac
import hashlib

# Compute SHA256 hex digest signature using auth token and payload.
auth_token = 'xxx-xxx-xxx'
signature = hmac.new(
    key=auth_token.encode('ascii'),
    msg=data.encode('ascii'),
    digestmod=hashlib.sha256
).hexdigest()

# Send test webhook request with computed signature in header.
response = requests.post(
    webhook_url,
    data=json.dumps(data),
    headers={
        'X-Viber-Content-Signature': signature,
        'Content-Type': 'application/json'
    },
    verify='E:\\Docs\\learn_py\\viberbot\\certificate.pem'
)


https://stackoverflow.com/questions/54997832/how-to-send-message-to-viber-bot-with-python
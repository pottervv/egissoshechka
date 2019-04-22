import logging

from aioviber.bot import Bot
from aioviber.chat import Chat
from viberbot.api.viber_requests import ViberSubscribedRequest

logger = logging.getLogger(__name__)

bot = Bot(
    name='helpegisso',
    avatar='http://egisso.ru/site/img/family.efd5d97b4a8a3b65d467d2ad40303706.png',
    auth_token='496bdc821627d6e3-89019a2a752a3f08-58f225f6ba43594',  # Public account auth token
    host="my.host.com",  # should be available from wide area network
    port=443,
    webhook="https://egissoshechka.herokuapp.com",  # Webhook url
)

@bot.command('ping')
async def ping(chat: Chat, matched):
    await chat.send_text('pong')

@bot.event_handler('subscribed')
async def user_subscribed(chat: Chat, request: ViberSubscribedRequest):
    await chat.send_text('Welcome')

@bot.message_handler('sticker')
async def sticker(chat: Chat):
    await chat.send_sticker(5900)

if __name__ == '__main__':  # pragma: no branch
    bot.run()  # pragma: no cover
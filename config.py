from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration

bot_configuration = BotConfiguration(
	name = 'helpegisso',
	avatar = 'http://viber.com/avatar.jpg',
	auth_token = '496bdc821627d6e3-89019a2a752a3f08-58f225f6ba43594'
)
viber = Api(bot_configuration)
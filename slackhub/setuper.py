from slackbot.bot import respond_to

from slackhub.permissioner import get_user_id
from slackhub.persister import list_admins, save_admin

"""
Handles setup of the bot.
"""


@respond_to('init')
def init_admin(message):
    """
    Initialize the bot. This is primarily to setup the first admin user. Will do nothing
    as long as there are any admin users defined.
    :param message: message body that holds things like the user and how to reply
    """
    if list_admins():
        message.reply('System is already setup.')
    else:
        admin = get_user_id(message)
        save_admin(admin)
        message.reply(admin + ' added as initial admin.')

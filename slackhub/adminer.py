from slackbot.bot import respond_to

from slackhub.dispatcher import get_slack_username
from slackhub.persister import save_admin, list_admins

"""
Handles admin configuration of the system.
"""


@respond_to('add admin (.*)')
def add_admin(message, admin):
    if verify_admin(message):
        save_admin(admin)
        message.reply('Admin [*' + admin + '*] has been added.')
    else:
        message.reply('Access denied')


@respond_to('list admins')
def list_admin(message):
    if verify_admin(message):
        admin_names = []
        for user_id in list_admins():
            admin_names.append(get_slack_username(user_id))
        message.reply('Current admins: ' + str(admin_names))
    else:
        message.reply('Access denied')


def get_user_id(message):
    """
    Get the user id from the message body
    :param message: message body to parse
    :return: user id from the message
    """
    return message.user['id']


def get_username(message):
    """
    Get the username from the message body
    :param message: message body to parse
    :return: username from the message
    """
    return message.user['name']


def verify_admin(message):
    """
    Verify that the user performing the operation is one of the known admins
    :param message: message bogy to parse
    :return: boolean whether user is an admin or not
    """
    if get_user_id(message) in list_admins():
        return True
    else:
        return False

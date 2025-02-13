import logging
from dotenv import load_dotenv
from slack_sdk import WebClient

import slackhub.utiler as utiler

"""
Handles message posting to slack.
"""

# load env needs to be called here because reasons? Maybe because flask is distributing messages to their own thread?
load_dotenv()

# direct access to the slack API when needed for special actions
slack_token = utiler.get_env('SLACK_BOT_TOKEN')
client = WebClient(token=slack_token)

logger = logging.getLogger(__name__)


def post_message(channel, attachments):
    """
    Post the message based off the attachment to user in slack.
    :param channel: user who should receive the message
    :param attachments: array of attachment objects that hold slack's complex formatted message
    """
    logger.debug('sending to channel [%s]: %s', channel, attachments)

    client.chat_postMessage(channel=channel,
                            attachments=attachments,
                            unfurl_links=False,
                            unfurl_media=False)


def get_slack_channel_name(channel_id):
    """
    Get the username of the slack user by their id
    :param channel_id: id of the user
    :return: username of the user
    """
    channel = client.conversations_info(channel=channel_id)
    return channel['channel']['name']


def get_slack_username(user_id):
    """
    Get the username of the slack user by their id
    :param user_id: id of the user
    :return: username of the user
    """
    user = client.users_info(user=user_id)
    return user['user']['name']

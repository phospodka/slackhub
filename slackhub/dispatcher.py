import json
from slackbot import settings
from slacker import Slacker

"""
Handles message posting to slack.
"""

# direct access to the slack API when needed for special actions
slack = Slacker(settings.API_TOKEN)


def post_message(channel, usertype, attachments):
    """
    Post the message based off the attachment to user in slack.
    :param channel: user who should receive the message
    :param usertype: type of user to send to
    :param attachments: array of attachment objects that hold slack's complex formatted message
    """
    # channel = '@' + channel if usertype == 'user' else channel  # maybe externalise this logic
    slack.chat.post_message(channel,                      # channel / user to message
                            None,                         # plain text to send
                            settings.BOT_NAME,            # username to reply as
                            settings.BOT_NAME,            # as user to masquerade as
                            None,                         # parse
                            None,                         # link names
                            attachments,                  # attachments for fancy text
                            False,                        # unfurl links
                            False)                        # unfurl media


def get_slack_username(user_id):
    user = json.loads(slack.users.info(user_id).raw)
    return user['user']['name']
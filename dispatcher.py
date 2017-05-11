from slackbot import settings
from slackhub.slackhubbot import slack

"""
Handles message posting to slack.
"""


def post_message(channel, usertype, attachment):
    """
    Post the message based off the attachment to user in slack.
    :param channel: user who should receive the message
    :param usertype: type of user to send to
    :param attachment: object that holds the parts of the message
    """
    channel = '@' + channel if usertype == 'user' else channel  # maybe externalise this logic
    slack.chat.post_message(channel,                      # channel / user to message
                            format_message(attachment),   # text to send
                            settings.BOT_NAME,            # username to reply as
                            settings.BOT_NAME,            # as user to masquerade as
                            None,                         # parse
                            None,                         # link names
                            None,                         # attachments
                            False,                        # unfurl links
                            False)                        # unfurl media


def bold_title(title):
    """
    Bold and format a title text
    :param title: title to format
    :return: formatted title
    """
    return '*' + title.strip() + '*' + '\n'


def format_message(message):
    """
    Format the message so it is not just plain text and can stand out a little
    :param message: message to format
    :return: formatted message
    """
    # return message['pretext'] + '\n' + '> ' + bold_title(message['title']) + '> ' + message['text']
    pretext = message.get('pretext', None)
    title = message.get('title', None)
    title_link = message.get('title_link', None)
    text = message.get('text', None)
    footer = message.get('footer', None)

    reply = ''

    if pretext is not None:
        reply += pretext + '\n'

    if title is not None:
        if title_link is not None:
            reply += '> ' + '<' + title_link + '|' + title + '>' + '\n'
        else:
            reply += '> ' + bold_title(title)

    if text is not None:
        reply += '> ' + text

    if footer is not None:
        reply += '\n' + '> ' + footer

    return reply

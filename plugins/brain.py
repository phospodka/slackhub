import json
import os
import sys

from slackbot import settings
from slackbot.bot import listen_to
from slackbot.bot import respond_to
from slacker import Slacker

slack = Slacker(settings.API_TOKEN)

"""
This is the brain of the slackhub bot.  It does all the subscription management and listening to messages.
It uses a special message text (#bot_text) from a modified slackbot base that can work with messages from
other bots.

A couple times it has to use the slacker API directly to do more advanced operations.

Doc strings for methods with @respond_to will look odd because they are exposed by the bot to slack.
"""


# the all important cache of users; all important.
cache = {}


@respond_to('add (branch|mention) (.*)')
def add_actions(message, action, target):
    """
    Add subscriptions of a branch or mention.  i.e. add mention username
    """
    """
    Add subscriptions of a branch or mention for the requesting user.  Reply to the user informing what they requested.
    :param message: message body that holds things like the user and how to reply
    :param action: type of subscription to add (branch or mention)
    :param target: text that represents what to subscribe to
    """
    username = get_username(message)
    subs = load_user(username)

    if subs:
        try:
            my_set = set(subs[action])
            my_set.add(target)
            subs[action] = list(my_set)
        except KeyError:
            my_set = set()
            my_set.add(target)
            subs[action] = list(my_set)
    else:
        # subs = {'user': username, action: [target], 'enabled': True}
        subs = {action: [target], 'enabled': True}

    save_user(subs, username)
    message.reply('Subscribed to ' + action + ' [*' + target + '*]')


@respond_to('list (all|branch|mention)')
def list_actions(message, action):
    """
    List stored details for a user.  i.e. list mention
    """
    """
    List available values for a requesting user.  Options are everything about the user, branch subscriptions, and
    mention subscriptions.  Reply with the values.
    :param message: message body that holds things like the user and how to reply
    :param action: what type of information to list
    """
    username = get_username(message)
    data = ''

    try:
        if action == 'all':
            data = json.dumps(load_user(username))
        elif action == 'branch':
            data = json.dumps(load_user(username)['branch'])
        elif action == 'mention':
            data = json.dumps(load_user(username)['mention'])
    except KeyError:
        pass

    message.reply('You are subscribed to the following: ' + data)


@respond_to('remove (branch|mention) (.*)')
def remove_actions(message, action, target):
    """
    Remove subscriptions of a branch or mention.  i.e. remove mention username
    """
    """
    Remove subscriptions of a branch or mention for the requesting user.  Reply to the user informing what they
    requested.
    :param message: message body that holds things like the user and how to reply
    :param action: type of subscription to remove (branch or mention)
    :param target: text that represents what to unsubscribe from
    """
    username = get_username(message)
    subs = load_user(username)

    if subs:
        try:
            my_set = set(subs[action])
            my_set.remove(target)
            subs[action] = list(my_set)
        except KeyError:
            pass

    save_user(subs, username)
    message.reply('Unsubscribed from ' + action + ' [*' + target + '*]')


@listen_to('boop')
def listen(message):
    if cache == {}:
        populate_cache()

    for key, value in cache.items():
        print(key + ' ' + str(value))

    # print message.body['text']
    print(message.body.keys())
    slack.chat.post_message('@phospodka',
                            'Beep ' + message.body['text'],
                            'boop-bot')


@listen_to('#bot_text')
def github_mentions(message):
    """
    Super special listener for github message processing.
    :param message: message body that contains all the info
    """
    #print(message.body.keys())
    # get the message text so we can process it for subscriptions
    attachments = message.body['attachments'][0]
    text = attachments.get('text', '')
    title = attachments.get('title', '')
    print(json.dumps(attachments))

    if cache == {}:
        populate_cache()

    # process message text against all subscriptions
    for user, subs in cache.items():
        mentions = subs['mention']
        branches = subs['branch']

        # super hacky way to only look at comments
        if 'comment by' in title.lower():
            for m in mentions:
                if m in text:
                    slack.chat.post_message('@' + user,
                                            'Mention match!\n' + format_message(attachments),
                                            settings.BOT_NAME,
                                            settings.BOT_NAME,
                                            None,
                                            None,
                                            None,
                                            False,
                                            False)
                    break  # only notify once per user

        for b in branches:
            pass


def get_username(msg):
    """
    Get the username from the message body
    :param msg: message body to parse
    :return: username from the message
    """
    msguser = json.loads(slack.users.info(msg.body['user']).raw)
    return msguser['user']['name']


def format_message(message):
    """
    Format the message so it is not just plain text and can stand out a little
    :param message: message to format
    :return: formatted message
    """
    # return message['pretext'] + '\n' + '> ' + bold_title(message['title']) + '> ' + message['text']
    pretext = message.get('pretext', None)
    title = message.get('title', None)
    text = message.get('text', None)

    reply = ''

    if pretext is not None:
        reply += pretext + '\n'

    if title is not None:
        reply += '> ' + bold_title(title)

    if text is not None:
        reply += '> ' + text

    return reply


def bold_title(title):
    """
    Bold and format a title text
    :param title: title to format
    :return: formatted title
    """
    return '*' + title.strip() + '*' + '\n'


def save_user(data, user):
    """
    Save user to the cache and to persistent file
    :param data: data to save
    :param user: username data belongs to
    """
    if cache == {}:
        populate_cache()
    cache[user] = data
    write_user_to_file(data, user)


def write_user_to_file(data, user):
    """
    Write the user json data out to file
    :param data: data to write
    :param user: user to write data for
    """
    homedir = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(homedir + '/data/' + user, 'w') as f:
        f.write(json.dumps(data))


def load_user(user):
    """
    Load the user from the cache; populate as necessary
    :param user: username to load
    :return: user data as a Python object
    """
    if cache == {}:
        populate_cache()

    return cache[user]


def load_user_from_file(user):
    """
    Load the user json data from file and return as a Python object structure.
    :param user: username to load
    :return: user data as a Python object
    """
    homedir = os.path.dirname(os.path.realpath(sys.argv[0]))

    # open the file for reading if it exist, if it does not we are okay with that
    try:
        with open(homedir + '/data/' + user, 'r+') as f:
            for line in f:
                if user in line:
                    return json.loads(line)
    except FileNotFoundError:
        pass


def list_users():
    homedir = os.path.dirname(os.path.realpath(sys.argv[0]))
    return next(os.walk(homedir + '/data/'))[2]


def populate_cache():
    """
    Walk the persistent file directory and populate the cache
    """
    path = os.path.dirname(os.path.realpath(sys.argv[0])) + '/data/'
    # paths = [os.path.join(path, fn) for fn in next(os.walk(path))[2]]
    usernames = next(os.walk(path))[2]

    for username in usernames:
        with open(path + username, 'r+') as f:
            for line in f:
                user = json.loads(line)
                cache[username] = user
                # cache.update(user)


def get_optional_message_text(message, key):
    pass

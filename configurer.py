import json

from slackbot.bot import respond_to
from slackhub.slackhubbot import get_username
from slackhub.persister import load_user
from slackhub.persister import save_user

"""
Handles user configuration of notifications.
"""


@respond_to('add (branch|mention) (.*)')
def add_actions(message, action, target):
    """
    Add subscriptions of a branch or mention.  Only mention is currently functional i.e. `add mention username`
    """
    """
    Add subscriptions of a branch or mention for the requesting user.  Reply to the user informing
    what they requested.
    :param message: message body that holds things like the user and how to reply
    :param action: type of subscription to add (branch or mention)
    :param target: text that represents what to subscribe to
    """
    username = get_username(message)
    subs = load_user(username)

    # if the user does not exist then create the subscription template
    if not subs:
        subs = {'mention': [], 'branch': [], 'enabled': True}

    try:
        my_set = set(subs[action])
        my_set.add(target)
        subs[action] = list(my_set)
    except KeyError:
        my_set = set()
        my_set.add(target)
        subs[action] = list(my_set)

    save_user(subs, username)
    message.reply('Subscribed to ' + action + ' [*' + target + '*]')


@respond_to('list (all|branch|mention)')
def list_actions(message, action):
    """
    List stored details for a user.  i.e. `list mention`
    """
    """
    List available values for a requesting user.  Options are everything about the user, branch
    subscriptions, and mention subscriptions.  Reply with the values.
    :param message: message body that holds things like the user and how to reply
    :param action: what type of information to list
    """
    username = get_username(message)
    data = None

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
    Remove subscriptions of a branch or mention.  i.e. `remove mention username`
    """
    """
    Remove subscriptions of a branch or mention for the requesting user.  Reply to the user
    informing what they requested.
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

import json

from slackbot.bot import respond_to
from slackhub.slackhubbot import get_username
from slackhub.persister import load_user
from slackhub.persister import save_user

"""
Handles user configuration of notifications.
"""


@respond_to('list (all|branch|enabled|label|mention|username)')
def list_actions(message, action):
    """
    List stored details for a user.  i.e. `list mention`
    """
    """
    List available values for a requesting user.  Options are everything about the user, branch
    label, and mention subscriptions.  Reply with the values.
    :param message: message body that holds things like the user and how to reply
    :param action: what type of information to list
    """
    username = get_username(message)
    data = None

    try:
        if action == 'all':
            data = json.dumps(load_user(username))
        else:
            data = json.dumps(load_user(username)[action])

    except KeyError:
        pass

    message.reply('Your settings for [*' + action + '*] are as follows: ' + data)


@respond_to('add (branch|label|mention) (.*)')
def add_actions(message, action, target):
    """
    Add subscriptions of a branch, label, or mention.  Only mention and label are currently functional i.e. `add mention username`
    """
    """
    Add subscriptions of a branch, label,  or mention for the requesting user.  Reply to the user
    informing what they requested.
    :param message: message body that holds things like the user and how to reply
    :param action: type of subscription to add (branch or mention)
    :param target: text that represents what to subscribe to
    """
    username = get_username(message)
    details = load_user(username)

    # if the user does not exist then create the subscription template
    if not details:
        details = {'mention': [],
                   'branch': [],
                   'label': [],
                   'enabled': {
                       'branch': True,
                       'label': True,
                       'mention': True,
                       'review': True},
                   'type': 'user',
                   'username': username}

    try:
        my_set = set(details[action])
        my_set.add(target)
        details[action] = list(my_set)
    except KeyError:
        my_set = set()
        my_set.add(target)
        details[action] = list(my_set)

    save_user(details, username)
    message.reply('Subscribed to ' + action + ' [*' + target + '*]')


@respond_to('remove (branch|label|mention) (.*)')
def remove_actions(message, action, target):
    """
    Remove subscriptions of a branch, label, or mention.  i.e. `remove mention username`
    """
    """
    Remove subscriptions of a branch, label, or mention for the requesting user.  Reply to the user
    informing what they requested.
    :param message: message body that holds things like the user and how to reply
    :param action: type of subscription to remove (branch or mention)
    :param target: text that represents what to unsubscribe from
    """
    username = get_username(message)
    details = load_user(username)

    if details:
        try:
            my_set = set(details[action])
            my_set.remove(target)
            details[action] = list(my_set)
        except KeyError:
            pass

    save_user(details, username)
    message.reply('Unsubscribed from ' + action + ' [*' + target + '*]')


@respond_to('disable (all|branch|label|mention|review)')
def disable_notifications(message, target):
    """
    Disable notifications selectively or for all while preserving settings.  i.e. `disable branch`
    """
    '''
    Disable notifications for the requesting user.  Preserves settings so they can be disabled at
    will.
    :param message: message body that holds things like the user and how to reply
    :param target: type of notification to disable
    '''
    username = get_username(message)
    details = load_user(username)

    if details:
        try:
            if target == 'all':
                for key in details['enabled'].keys():
                    details['enabled'][key] = False
            else:
                details['enabled'][target] = False
        except KeyError:
            pass

    save_user(details, username)
    message.reply('Disabled [*' + target + '*].  Can be re-enabled using: _enable ' + target + '_')


@respond_to('enable (all|branch|label|mention|review)')
def enable_notifications(message, target):
    """
    Enable notifications selectively or for all while preserving settings.  i.e. `enable branch`
    """
    '''
    Enable notifications for the requesting user.  Preserves settings so they can be enabled at
    will.
    :param message: message body that holds things like the user and how to reply
    :param target: type of notification to enable
    '''
    username = get_username(message)
    details = load_user(username)

    if details:
        try:
            if target == 'all':
                for key in details['enabled'].keys():
                    details['enabled'][key] = True
            else:
                details['enabled'][target] = True
        except KeyError:
            pass

    save_user(details, username)
    message.reply('Enabled [*' + target + '*].  Can be disabled using: disable _' + target + '_')


@respond_to('username (.*)')
def set_username(message, username):
    """
    Set your github username to links notifications to this slack account.  i.e. `username batman`
    """
    '''
    Set the github username so we can link it to this slack user and provide notifications based on
    it.
    :param message: message body that holds things like the user and how to reply
    :param username: github username
    '''
    slack_username = get_username(message)
    details = load_user(slack_username)

    if details:
        try:
            details['username'] = username
        except KeyError:
            pass

    save_user(details, username)
    message.reply('Github username set as [*' + username + '*].')

import json

from slackbot.bot import respond_to
from slackhub.persister import list_repos, load_user, save_user

"""
Handles user configuration of notifications.
"""


@respond_to('list (all|enabled|label|mention|username)')
def list_actions(message, action):
    """
    List stored details for a user.  i.e. `list mention`
    """
    """
    List available values for a requesting user.  Options are everything about the user, 
    label, and mention subscriptions.  Reply with the values.
    :param message: message body that holds things like the user and how to reply
    :param action: what type of information to list
    """
    slack_id = get_user_id(message)
    data = None

    try:
        if action == 'all':
            data = json.dumps(load_user(slack_id))
        else:
            data = json.dumps(load_user(slack_id)[action])

    except KeyError:
        pass

    message.reply('Your settings for [*' + action + '*] are as follows: ' + data)


@respond_to('add (label|mention) (.*)')
def add_actions(message, action, target):
    """
    Add subscriptions of a label, or mention.  Only mention and label are currently functional i.e. `add mention username`
    """
    """
    Add subscriptions of a label,  or mention for the requesting user.  Reply to the user
    informing what they requested.
    :param message: message body that holds things like the user and how to reply
    :param action: type of subscription to add (label or mention)
    :param target: text that represents what to subscribe to
    """
    slack_id = get_user_id(message)
    details = get_details(slack_id)

    try:
        my_set = set(details[action])
        my_set.add(target)
        details[action] = list(my_set)
    except KeyError:
        my_set = set()
        my_set.add(target)
        details[action] = list(my_set)

    save_user(details, slack_id)
    message.reply('Subscribed to ' + action + ' [*' + target + '*]')


@respond_to('remove (label|mention) (.*)')
def remove_actions(message, action, target):
    """
    Remove subscriptions of a label, or mention.  i.e. `remove mention username`
    """
    """
    Remove subscriptions of a label, or mention for the requesting user.  Reply to the user
    informing what they requested.
    :param message: message body that holds things like the user and how to reply
    :param action: type of subscription to remove (label or mention)
    :param target: text that represents what to unsubscribe from
    """
    slack_id = get_user_id(message)
    details = get_details(slack_id)

    if details:
        try:
            my_set = set(details[action])
            my_set.remove(target)
            details[action] = list(my_set)
        except KeyError:
            pass

    save_user(details, slack_id)
    message.reply('Unsubscribed from ' + action + ' [*' + target + '*]')


@respond_to('disable (all|label|mention|pr)')
def disable_notifications(message, target):
    """
    Disable notifications selectively or for all while preserving settings.  i.e. `disable mention`
    """
    '''
    Disable notifications for the requesting user.  Preserves settings so they can be disabled at
    will.
    :param message: message body that holds things like the user and how to reply
    :param target: type of notification to disable
    '''
    slack_id = get_user_id(message)
    details = get_details(slack_id)

    if details:
        try:
            if target == 'all':
                for key in details['enabled'].keys():
                    details['enabled'][key] = False
            else:
                details['enabled'][target] = False
        except KeyError:
            pass

    save_user(details, slack_id)
    message.reply('Disabled [*' + target + '*].  Can be re-enabled using: _enable ' + target + '_')


@respond_to('enable (all|label|mention|pr)')
def enable_notifications(message, target):
    """
    Enable notifications selectively or for all while preserving settings.  i.e. `enable mention`
    """
    '''
    Enable notifications for the requesting user.  Preserves settings so they can be enabled at
    will.
    :param message: message body that holds things like the user and how to reply
    :param target: type of notification to enable
    '''
    slack_id = get_user_id(message)
    details = get_details(slack_id)

    if details:
        try:
            if target == 'all':
                for key in details['enabled'].keys():
                    details['enabled'][key] = True
            else:
                details['enabled'][target] = True
        except KeyError:
            pass

    save_user(details, slack_id)
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
    slack_id = get_user_id(message)
    details = get_details(slack_id)

    if details:
        try:
            details['username'] = username
        except KeyError:
            pass

    save_user(details, slack_id)
    message.reply('Github username set as [*' + username + '*].')


@respond_to('repos')
def list_repositories(message):
    """
    List the repositories being watched
    """
    '''
    List the repositories being watched and used by the system.
    :param message: message body that holds things like the user and how to reply
    '''
    repos = list_repos()

    reply = '```'
    for repo in repos:
        reply += '\n' + repo
    reply += '```'

    message.reply('The following repos are being watched:' + reply)


def get_details(slack_id):
    """
    Get the details about a user and create the template if they do not exist yet
    :param slack_id: slack username to lookup user by
    :return: set of details about user
    """
    details = load_user(slack_id)

    # if the user does not exist then create the subscription template
    if not details:
        details = {'mention': [],
                   'label': [],
                   'enabled': {
                       'label': True,
                       'mention': True,
                       'pr': True},
                   'repo': [],
                   'type': 'user',
                   'username': slack_id} # ?

    return details


def get_user_id(message):
    """
    Get the user id from the message body
    :param message: message body to parse
    :return: user id from the message
    """
    return message.user['id']

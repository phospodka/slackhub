import json

from slackbot.bot import respond_to

from slackhub.dispatcher import get_slack_username, get_slack_channel_name
from slackhub.permissioner import verify_admin
from slackhub.persister import save_admin, list_admins, load_channel, save_channel

"""
Handles admin configuration of the system.
"""


@respond_to('add admin (.*)')
@verify_admin
def add_admin(message, admin):
    """
    Add user to the list of admins. e.g. add admin username
    """
    """
    Add user to the list of admins.  Will throw error if requesting user is not an admin.
    :param message: message body that holds things like the user and how to reply 
    :param admin: username to add as admin
    """
    save_admin(admin)
    message.reply('Admin [*' + admin + '*] has been added.')


@respond_to('list admin')
def list_admin(message):
    """
    List current admins. e.g. list admin
    """
    """
    Get the list of current admins.
    :param message: message body that holds things like the user and how to reply 
    """
    admin_names = []
    for user_id in list_admins():
        admin_names.append(get_slack_username(user_id))
    message.reply('Current admins: ' + str(admin_names))


@respond_to('add channel ([\w-]+) (label|mention) (.+)')
@verify_admin
def add_channel_actions(message, channel_id, action, target):
    """
    Add subscriptions of a label, or mention to a channel. e.g. `add channel C012345 mention username`
    """
    """
    Add subscriptions of a label, or mention for the specified channel.  Reply to the admin
    informing what they requested.
    :param message: message body that holds things like the user and how to reply
    :param channel_id: channel id to add actions for
    :param action: type of subscription to add (label or mention)
    :param target: text that represents what to subscribe to
    """
    details = get_channel_details(channel_id)

    try:
        my_set = set(details[action])
        my_set.add(target)
        details[action] = list(my_set)
    except KeyError:
        my_set = set()
        my_set.add(target)
        details[action] = list(my_set)

    save_channel(details, channel_id)
    message.reply('#' + details.get('username') + ' subscribed to ' + action + ' [*' + target + '*]')


@respond_to('list channel ([\w-]+) (all|enabled|label|mention|repo|username)')
@verify_admin
def list_channel_actions(message, channel_id, action):
    """
    List stored details for a channel. e.g. `list channel C012345 all`
    """
    """
    List available values for a specified channel.  Options are everything about the channel, 
    label, and mention subscriptions.  Reply with the values.
    :param message: message body that holds things like the user and how to reply
    :param channel_id: channel id to lookup information for
    :param action: what type of information to list
    """
    try:
        if action == 'all':
            data = load_channel(channel_id)
        else:
            data = load_channel(channel_id)[action]

    except KeyError:
        data = None

    if data is not None:
        reply = '```' + json.dumps(data, indent=4, sort_keys=True) + '```'
        message.reply('Your settings for [*' + action + '*] are as follows: ' + reply)
    else:
        message.reply('No channel data found')


@respond_to('remove channel ([\w-]+) (label|mention) (.+)')
@verify_admin
def remove_actions(message, channel_id, action, target):
    """
    Remove subscriptions of a label, or mention to a channel. e.g. `remove channel C012345 mention username`
    """
    """
    Remove subscriptions of a label, or mention for the specified channel.  Reply to the admin
    informing what they requested.
    :param message: message body that holds things like the user and how to reply
    :param channel_id: channel id to add actions for
    :param action: type of subscription to remove (label or mention)
    :param target: text that represents what to unsubscribe from
    """
    details = get_channel_details(channel_id)

    try:
        my_set = set(details[action])
        my_set.remove(target)
        details[action] = list(my_set)
    except KeyError:
        pass

    save_channel(details, channel_id)
    message.reply('#' + details.get('username') + ' unsubscribed from ' + action + ' [*' + target + '*]')


def get_channel_details(channel_id):
    """
    Get the details about a user and create the template if they do not exist yet
    :param channel_id: slack username to lookup user by
    :return: set of details about user; will not return None
    """
    details = load_channel(channel_id)

    # if the user does not exist then create the subscription template
    if not details:
        channel = get_slack_channel_name(channel_id)
        details = {'mention': [],
                   'label': [],
                   'enabled': {
                       'label': True,
                       'mention': True,
                       'pr': True},
                   'repo': [],
                   'type': 'channel',
                   'username': channel}

    return details

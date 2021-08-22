import json

from slackbot.bot import respond_to

from slackhub.commander import list_channel, add_details, add_repo, add_repo_details, \
    remove_details, remove_repo, remove_repo_details, disable_feature, disable_repo_feature, \
    enable_feature, enable_repo_feature
from slackhub.dispatcher import get_slack_username, get_slack_channel_name
from slackhub.permissioner import verify_admin
from slackhub.persister import save_admin, list_admins, load_channel

"""
Handles admin configuration of the system.
"""


@respond_to('add admin (.*)')
@verify_admin
def add_admin(message, admin):
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
    Get the list of current admins.
    :param message: message body that holds things like the user and how to reply 
    """
    admin_names = []
    for user_id in list_admins():
        admin_names.append(get_slack_username(user_id))
    message.reply('Current admins: ' + str(admin_names))


@respond_to('list channel ([\\w-]+) (all|enabled|label|mention|repo|username)')
@verify_admin
def list_channel_actions(message, channel_id, action):
    """
    List available values for a specified channel.  Options are everything about the channel, 
    label, and mention subscriptions.  Reply with the values.
    :param message: message body that holds things like the user and how to reply
    :param channel_id: channel id to lookup information for
    :param action: what type of information to list
    """
    data = list_channel(channel_id, action)

    if data is not None:
        reply = '```' + json.dumps(data, indent=4, sort_keys=True) + '```'
        message.reply('Your settings for [*' + action + '*] are as follows: ' + reply)
    else:
        message.reply('No channel data found')


@respond_to('add channel ([\\w-]+) (label|mention) (.+)')
@verify_admin
def add_channel_actions(message, channel_id, action, target):
    """
    Add subscriptions of a label, or mention for the specified channel.  Reply to the admin
    informing what they requested.
    :param message: message body that holds things like the user and how to reply
    :param channel_id: channel id to add actions for
    :param action: type of subscription to add (label or mention)
    :param target: text that represents what to subscribe to
    """
    details = _get_channel_details(channel_id)
    add_details(channel_id, details, action, target)
    message.reply('#' + details.get('username') + ' subscribed to ' + action + ' [*' + target + '*]')


@respond_to('add channel ([\\w-]+) repo ([\\w-]+) (label|mention) (.+)')
@verify_admin
def add_channel_repo_actions(message, channel_id, name, action, target):
    """
    Add subscriptions of a label, or mention to a repository for the requesting user.  Reply to the 
    user informing what they requested.
    :param message: message body that holds things like the user and how to reply
    :param channel_id: channel id to add repo actions for
    :param action: type of subscription to add (label or mention)
    :param target: text that represents what to subscribe to
    """
    repo_config = _get_channel_repo_config(channel_id, name)
    add_repo_details(channel_id, repo_config, name, action, target)
    message.reply('Subscribed to ' + action + ' [*' + target + '*] in repo *' + name + '*')


@respond_to('add channel ([\\w-]+) repo ([\\w-]+)$')
@verify_admin
def add_channel_repos(message, channel_id, name):
    """
    Add a repository subscription to the user.  This will default the enabled flags for that 
    repository and will require further commands to configure what else to notify on.  Reply
    to the user informing that they added the repo.
    :param message: message body that holds things like the user and how to reply
    :param channel_id: channel id to add repo for
    :param name: repository name to add
    """
    repo_config = _get_channel_repo_config(channel_id, name)
    add_repo(channel_id, repo_config, name)
    message.reply('Subscribed to repository ' + ' [*' + name + '*]')


@respond_to('remove channel ([\\w-]+) (label|mention) (.+)')
@verify_admin
def remove_channel_actions(message, channel_id, action, target):
    """
    Remove subscriptions of a label, or mention for the specified channel.  Reply to the admin
    informing what they requested.
    :param message: message body that holds things like the user and how to reply
    :param channel_id: channel id to remove actions for
    :param action: type of subscription to remove (label or mention)
    :param target: text that represents what to unsubscribe from
    """
    details = _get_channel_details(channel_id)
    remove_details(channel_id, details, action, target)
    message.reply('#' + details.get('username') + ' unsubscribed from ' + action + ' [*' + target + '*]')


@respond_to('remove channel ([\\w-]+) repo ([\\w-]+) (label|mention) (.+)')
@verify_admin
def remove_channel_repo_actions(message, channel_id, name, action, target):
    """
    Remove subscriptions of a label, or mention for the requesting user.  Reply to the user
    informing what they requested.
    :param message: message body that holds things like the user and how to reply
    :param channel_id: channel id to remove repo actions for
    :param action: type of subscription to remove (label or mention)
    :param target: text that represents what to unsubscribe from
    """
    repo_config = _get_channel_repo_config(channel_id, name)
    remove_repo_details(channel_id, repo_config, action, target)
    message.reply('Unsubscribed from ' + action + ' [*' + target + '*] in repo *' + name + '*')


@respond_to('remove channel ([\\w-]+) repo ([\\w-]+)$')
@verify_admin
def remove_channel_repos(message, channel_id, name):
    """
    Remove a repository subscription from the user.  Reply to the user informing that they 
    removed the repo.
    :param message: message body that holds things like the user and how to reply
    :param channel_id: channel id to remove repo for
    :param name: repository name to remove
    """
    repo_config = _get_channel_repo_config(channel_id, name)
    remove_repo(channel_id, repo_config)
    message.reply('Unsubscribed from repository ' + ' [*' + name + '*]')


@respond_to('disable channel ([\\w-]+) (all|label|mention|pr)')
@verify_admin
def disable_notifications(message, channel_id, target):
    """
    Disable notifications for the requesting user.  Preserves settings so they can be disabled at
    will.
    :param message: message body that holds things like the user and how to reply
    :param channel_id: channel id to disable notifications for
    :param target: type of notification to disable
    """
    details = _get_channel_details(channel_id)
    disable_feature(channel_id, details, target)
    message.reply('Disabled [*' + target + '*].  Can be re-enabled using: _enable ' + target + '_')


@respond_to('disable channel ([\\w-]+) repo ([\\w-]+) (all|label|maintainer|mention|pr)')
@verify_admin
def disable_repo_notifications(message, channel_id, name, target):
    """
    Disable notifications on a repository for the requesting user.  Preserves settings so they can
    be disabled at will.
    :param message: message body that holds things like the user and how to reply
    :param channel_id: channel id to disable repo notifications for
    :param target: type of notification to disable
    """
    repo_config = _get_channel_repo_config(channel_id, name)
    disable_repo_feature(channel_id, repo_config, target)
    message.reply('Disabled [*' + target + '*] on repo ' + name
                  + '.  Can be re-enabled using: _enable repo ' + name + ' ' + target + '_')


@respond_to('enable channel ([\\w-]+) (all|label|mention|pr)')
@verify_admin
def enable_notifications(message, channel_id, target):
    """
    Enable notifications for the requesting user.  Preserves settings so they can be enabled at
    will.
    :param message: message body that holds things like the user and how to reply
    :param channel_id: channel id to enable notifications for
    :param target: type of notification to enable
    """
    details = _get_channel_details(channel_id)
    enable_feature(channel_id, details, target)
    message.reply('Enabled [*' + target + '*].  Can be disabled using: _disable ' + target + '_')


@respond_to('enable channel ([\\w-]+) repo ([\\w-]+) (all|label|maintainer|mention|pr)')
@verify_admin
def enable_repo_notifications(message, channel_id, name, target):
    """
    Enable notifications on a repository for the requesting user.  Preserves settings so they can be 
    enabled at will.
    :param message: message body that holds things like the user and how to reply
    :param channel_id: channel id to enable repo notifications for
    :param target: type of notification to enable
    """
    repo_config = _get_channel_repo_config(channel_id, name)
    enable_repo_feature(channel_id, repo_config, target)
    message.reply('Enabled [*' + target + '*] on repo ' + name
                  + '.  Can be disabled using: _disable repo ' + name + ' ' + target + '_')


def _get_channel_details(channel_id):
    """
    Get the details about a user and create the template if they do not exist yet
    :param channel_id: slack username to lookup user by
    :return: set of details about user; will not return None
    """
    details = load_channel(channel_id)

    # if the channel does not exist then create the subscription template
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


def _get_channel_repo_config(channel_id, name):
    """
    Get the repo config of a repository for a channel.  This will be a tuple of the user details,
    the repo list, and the requested repo.
    :param channel_id: channel id to get repo config for
    :param name: repository
    :return: tuple of ({details}, [repo], repo); None for positions not found
    """
    details = _get_channel_details(channel_id)

    try:
        repos = details['repo']

        for repo in repos:
            if repo.get('name') == name:
                return details, repos, repo

        return details, repos, None
    except KeyError:
        pass

    return details, None, None

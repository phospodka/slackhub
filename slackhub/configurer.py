import json

from slackbot.bot import respond_to

from slackhub.commander import list_user, add_details, add_repo, add_repo_details, remove_details, \
    remove_repo, remove_repo_details, disable_feature, disable_repo_feature, enable_feature, \
    enable_repo_feature, save_username
from slackhub.permissioner import get_user_id
from slackhub.persister import list_repos, load_user

"""
Handles user configuration of notifications.
"""


@respond_to('list (all|enabled|label|mention|repo|username)')
def list_actions(message, action):
    """
    List available values for a requesting user.  Options are everything about the user, 
    label, and mention subscriptions.  Reply with the values.
    :param message: message body that holds things like the user and how to reply
    :param action: what type of information to list
    """
    slack_id = get_user_id(message)
    data = list_user(slack_id, action)

    if data is not None:
        reply = '```' + json.dumps(data, indent=4, sort_keys=True) + '```'
        message.reply('Your settings for [*' + action + '*] are as follows: ' + reply)
    else:
        message.reply('No user data found')


@respond_to('add (label|mention) (.+)')
def add_actions(message, action, target):
    """
    Add subscriptions of a label, or mention for the requesting user.  Reply to the user
    informing what they requested.
    :param message: message body that holds things like the user and how to reply
    :param action: type of subscription to add (label or mention)
    :param target: text that represents what to subscribe to
    """
    slack_id = get_user_id(message)
    details = _get_user_details(slack_id)
    add_details(slack_id, details, action, target)
    message.reply('Subscribed to ' + action + ' [*' + target + '*]')


@respond_to('add repo ([\\w-]+) (label|mention) (.+)')
def add_repo_actions(message, name, action, target):
    """
    Add subscriptions of a label, or mention to a repository for the requesting user.  Reply to the 
    user informing what they requested.
    :param message: message body that holds things like the user and how to reply
    :param action: type of subscription to add (label or mention)
    :param target: text that represents what to subscribe to
    """
    slack_id = get_user_id(message)
    repo_config = _get_repo_config(slack_id, name)
    add_repo_details(slack_id, repo_config, name, action, target)
    message.reply('Subscribed to ' + action + ' [*' + target + '*] in repo *' + name + '*')


@respond_to('add repo ([\\w-]+)$')
def add_repos(message, name):
    """
    Add a repository subscription to the user.  This will default the enabled flags for that 
    repository and will require further commands to configure what else to notify on.  Reply
    to the user informing that they added the repo.
    :param message: message body that holds things like the user and how to reply
    :param name: repository name to add
    """
    slack_id = get_user_id(message)
    repo_config = _get_repo_config(slack_id, name)
    add_repo(slack_id, repo_config, name)
    message.reply('Subscribed to repository ' + ' [*' + name + '*]')


@respond_to('remove (label|mention) (.+)')
def remove_actions(message, action, target):
    """
    Remove subscriptions of a label, or mention for the requesting user.  Reply to the user
    informing what they requested.
    :param message: message body that holds things like the user and how to reply
    :param action: type of subscription to remove (label or mention)
    :param target: text that represents what to unsubscribe from
    """
    slack_id = get_user_id(message)
    details = _get_user_details(slack_id)
    remove_details(slack_id, details, action, target)
    message.reply('Unsubscribed from ' + action + ' [*' + target + '*]')


@respond_to('remove repo ([\\w-]+) (label|mention) (.+)')
def remove_repo_actions(message, name, action, target):
    """
    Remove subscriptions of a label, or mention for the requesting user.  Reply to the user
    informing what they requested.
    :param message: message body that holds things like the user and how to reply
    :param action: type of subscription to remove (label or mention)
    :param target: text that represents what to unsubscribe from
    """
    slack_id = get_user_id(message)
    repo_config = _get_repo_config(slack_id, name)
    remove_repo_details(slack_id, repo_config, action, target)
    message.reply('Unsubscribed from ' + action + ' [*' + target + '*] in repo *' + name + '*')


@respond_to('remove repo ([\\w-]+)$')
def remove_repos(message, name):
    """
    Remove a repository subscription from the user.  Reply to the user informing that they 
    removed the repo.
    :param message: message body that holds things like the user and how to reply
    :param name: repository name to remove
    """
    slack_id = get_user_id(message)
    repo_config = _get_repo_config(slack_id, name)
    remove_repo(slack_id, repo_config)
    message.reply('Unsubscribed from repository ' + ' [*' + name + '*]')


@respond_to('disable (all|label|mention|pr)')
def disable_notifications(message, target):
    """
    Disable notifications for the requesting user.  Preserves settings so they can be disabled at
    will.
    :param message: message body that holds things like the user and how to reply
    :param target: type of notification to disable
    """
    slack_id = get_user_id(message)
    details = _get_user_details(slack_id)
    disable_feature(slack_id, details, target)
    message.reply('Disabled [*' + target + '*].  Can be re-enabled using: _enable ' + target + '_')


@respond_to('disable repo ([\\w-]+) (all|label|maintainer|mention|pr|prefix)')
def disable_repo_notifications(message, name, target):
    """
    Disable notifications on a repository for the requesting user.  Preserves settings so they can 
    be disabled at will.
    :param message: message body that holds things like the user and how to reply
    :param target: type of notification to disable
    """
    slack_id = get_user_id(message)
    repo_config = _get_repo_config(slack_id, name)
    disable_repo_feature(slack_id, repo_config, target)
    message.reply('Disabled [*' + target + '*] on repo ' + name
                  + '.  Can be re-enabled using: _enable repo ' + name + ' ' + target + '_')


@respond_to('enable (all|label|mention|pr)')
def enable_notifications(message, target):
    """
    Enable notifications for the requesting user.  Preserves settings so they can be enabled at
    will.
    :param message: message body that holds things like the user and how to reply
    :param target: type of notification to enable
    """
    slack_id = get_user_id(message)
    details = _get_user_details(slack_id)
    enable_feature(slack_id, details, target)
    message.reply('Enabled [*' + target + '*].  Can be disabled using: _disable ' + target + '_')


@respond_to('enable repo ([\\w-]+) (all|label|maintainer|mention|pr|prefix)')
def enable_repo_notifications(message, name, target):
    """
    Enable notifications on a repository for the requesting user.  Preserves settings so they can be 
    enabled at will.
    :param message: message body that holds things like the user and how to reply
    :param target: type of notification to enable
    """
    slack_id = get_user_id(message)
    repo_config = _get_repo_config(slack_id, name)
    enable_repo_feature(slack_id, repo_config, target)
    message.reply('Enabled [*' + target + '*] on repo ' + name
                  + '.  Can be disabled using: _disable repo ' + name + ' ' + target + '_')


@respond_to('username ([\\w-]+)$')
def set_username(message, username):
    """
    Set the github username so we can link it to this slack user and provide notifications based on
    it.
    :param message: message body that holds things like the user and how to reply
    :param username: github username
    """
    slack_id = get_user_id(message)
    details = _get_user_details(slack_id)
    save_username(slack_id, details, username)
    message.reply('Github username set as [*' + username + '*].')


@respond_to('repos')
def list_repositories(message):
    """
    List the repositories being watched and used by the system.
    :param message: message body that holds things like the user and how to reply
    """
    repos = list_repos()

    reply = '```'
    for repo in repos:
        reply += '\n' + repo
    reply += '```'

    message.reply('The following repos are being watched:' + reply)


def _get_repo_config(slack_id, name):
    """
    Get the repo config of a repository for a user.  This will be a tuple of the user details, 
    the repo list, and the requested repo.
    :param slack_id: user id to get repo config for
    :param name: repository
    :return: tuple of ({details}, [repo], repo); None for positions not found
    """
    details = _get_user_details(slack_id)

    try:
        repos = details['repo']

        for repo in repos:
            if repo.get('name') == name:
                return details, repos, repo

        return details, repos, None
    except KeyError:
        pass

    return details, None, None


def _get_user_details(slack_id):
    """
    Get the details about a user and create the template if they do not exist yet
    :param slack_id: slack username to lookup user by
    :return: set of details about user; will not return None
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
                   'username': slack_id}  # need a better default maybe?

    return details

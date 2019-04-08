import json

from slackbot.bot import respond_to
from slackhub.persister import list_repos, load_user, save_user

"""
Handles user configuration of notifications.
"""


@respond_to('list (all|enabled|label|mention|repo|username)')
def list_actions(message, action):
    """
    List stored details for a user. e.g. `list mention`
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


@respond_to('add (repo )?(label|mention) (.*)')
def add_actions(message, repo, action, target):
    """
    Add subscriptions of a label, or mention. e.g. `add mention username`
    """
    """
    Add subscriptions of a label, or mention for the requesting user.  Reply to the user
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


@respond_to('add repo (.*)')
def add_repo(message, name):
    """
    Add subscription to a repository. e.g. add repo slackhub
    """
    '''
    Add a repository subscription to the user.  This will default the enabled flags for that 
    repository and will require further commands to configure what else to notify on.  Reply
    to the user informing that they added the repo.
    :param message: message body that holds things like the user and how to reply
    :param name: repository name to add
    '''
    slack_id = get_user_id(message)
    details = get_details(slack_id)

    try:
        repos = details['repo']
        contains = False

        # look to see if the repo is already added
        for repo in repos:
            if repo.get('name') == name:
                contains = True

        # skip if the repo is added so we do not lose settings
        if not contains:
            repos.append(create_repo(name))
    except KeyError:
        repos = [create_repo(name)]
        details['repo'] = repos

    save_user(details, slack_id)
    message.reply('Subscribed to repository ' + ' [*' + name + '*]')


@respond_to('remove (repo )?(label|mention) (.*)')
def remove_actions(message, repo, action, target):
    """
    Remove subscriptions of a label, or mention. e.g. `remove mention username`
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


@respond_to('remove repo (.*)')
def remove_repo(message, name):
    """
    Remove subscription to a repository. e.g. remove repo slackhub
    """
    '''
    Remove a repository subscription from the user.  Reply to the user informing that they 
    removed the repo.
    :param message: message body that holds things like the user and how to reply
    :param name: repository name to remove
    '''
    slack_id = get_user_id(message)
    details = get_details(slack_id)

    if details:
        try:
            repos = details['repo']

            for repo in repos:
                print('name: ' + repo.get('name') + ' | ' + name + ' = ' + str(repo.get('name') == name))
                if repo.get('name') == name:
                    repos.remove(repo)
                    details['repo'] = repos
        except KeyError:
            pass

    save_user(details, slack_id)
    message.reply('Unsubscribed from repository ' + ' [*' + name + '*]')


@respond_to('disable (repo )?(all|label|maintainer|mention|pr)')
def disable_notifications(message, repo, target):
    """
    Disable notifications selectively or for all while preserving settings. e.g. `disable mention`
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


@respond_to('enable (repo )?(all|label|maintainer|mention|pr|)')
def enable_notifications(message, repo, target):
    """
    Enable notifications selectively or for all while preserving settings. e.g. `enable mention`
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
    Set your github username to links notifications to this slack account. e.g. `username batman`
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
                   'username': slack_id}  # need a better default maybe?

    return details


def create_repo(repo):
    """
    Create a repo json structure for the given repository name. Defaults enabled to all except
    maintainer.
    :param repo: repository name to create json structure for
    :return: a new repo json object
    """
    return {
        "name": repo,
        "mention": [],
        "label": [],
        "enabled": {
            "label": True,
            "pr": True,
            "mention": True,
            "maintainer": False
        }
    }


def get_user_id(message):
    """
    Get the user id from the message body
    :param message: message body to parse
    :return: user id from the message
    """
    return message.user['id']

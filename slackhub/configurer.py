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

    try:
        if action == 'all':
            data = load_user(slack_id)
        else:
            data = load_user(slack_id)[action]

    except KeyError:
        data = None

    if data is not None:
        reply = '```' + json.dumps(data, indent=4, sort_keys=True) + '```'
        message.reply('Your settings for [*' + action + '*] are as follows: ' + reply)
    else:
        message.reply('No user data found')


@respond_to('add (label|mention) (.+)')
def add_actions(message, action, target):
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
    details = get_user_details(slack_id)

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


@respond_to('add repo ([\w-]+) (label|mention) (.+)')
def add_repo_actions(message, name, action, target):
    """
    Add subscriptions of a label, or mention to a repository. e.g. `add repo slackhub mention username`
    """
    """
    Add subscriptions of a label, or mention to a repository for the requesting user.  Reply to the 
    user informing what they requested.
    :param message: message body that holds things like the user and how to reply
    :param action: type of subscription to add (label or mention)
    :param target: text that represents what to subscribe to
    """
    slack_id = get_user_id(message)
    repo_config = get_repo_config(slack_id, name)

    # if the repo is found, add to it
    # else if repos exist but not the repo, create the repo and add to it
    # else we need to create the repos list and add to it
    if repo_config[2]:
        try:
            my_set = set(repo_config[2][action])
            my_set.add(target)
            repo_config[2][action] = list(my_set)
        except KeyError:
            my_set = set()
            my_set.add(target)
            repo_config[2][action] = list(my_set)
    elif repo_config[1]:
        repo = create_repo(name)
        my_set = set()
        my_set.add(target)
        repo[action] = list(my_set)
        repo_config[1].append(repo)
    else:
        repo = create_repo(name)
        my_set = set()
        my_set.add(target)
        repo[action] = list(my_set)
        repos = [repo]
        repo_config[0]['repo'] = repos

    save_user(repo_config[0], slack_id)
    message.reply('Subscribed to ' + action + ' [*' + target + '*] in repo *' + name + '*')


@respond_to('add repo ([\w-]+)$')
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
    repo_config = get_repo_config(slack_id, name)

    # if we did not found the repo, add it
    # else if we did not find a repos list, create it and add the repo
    if not repo_config[2]:
        repo_config[1].append(create_repo(name))
    elif not repo_config[1]:
        repos = [create_repo(name)]
        repo_config[0]['repo'] = repos

    save_user(repo_config[0], slack_id)
    message.reply('Subscribed to repository ' + ' [*' + name + '*]')


@respond_to('remove (label|mention) (.+)')
def remove_actions(message, action, target):
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
    details = get_user_details(slack_id)

    try:
        my_set = set(details[action])
        my_set.remove(target)
        details[action] = list(my_set)
    except KeyError:
        pass

    save_user(details, slack_id)
    message.reply('Unsubscribed from ' + action + ' [*' + target + '*]')


@respond_to('remove repo ([\w-]+) (label|mention) (.+)')
def remove_repo_actions(message, name, action, target):
    """
    Remove subscriptions of a label, or mention from a repository. e.g. `remove repo slackhub mention username`
    """
    """
    Remove subscriptions of a label, or mention for the requesting user.  Reply to the user
    informing what they requested.
    :param message: message body that holds things like the user and how to reply
    :param action: type of subscription to remove (label or mention)
    :param target: text that represents what to unsubscribe from
    """
    slack_id = get_user_id(message)
    repo_config = get_repo_config(slack_id, name)

    # if the repo was found, remove the requested subscription
    if repo_config[2]:
        try:
            my_set = set(repo_config[2][action])
            my_set.remove(target)
            repo_config[2][action] = list(my_set)
        except KeyError:
            pass

    save_user(repo_config[0], slack_id)
    message.reply('Unsubscribed from ' + action + ' [*' + target + '*] in repo *' + name + '*')


@respond_to('remove repo ([\w-]+)$')
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
    repo_config = get_repo_config(slack_id, name)

    # if we found the repo, remove it
    if repo_config[2]:
        repo_config[1].remove(repo_config[2])

    save_user(repo_config[0], slack_id)
    message.reply('Unsubscribed from repository ' + ' [*' + name + '*]')


@respond_to('disable (all|label|mention|pr)')
def disable_notifications(message, target):
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
    details = get_user_details(slack_id)

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


@respond_to('disable repo ([\w-]+) (all|label|maintainer|mention|pr)')
def disable_repo_notifications(message, name, target):
    """
    Disable notifications on a repo selectively or for all while preserving settings. e.g. `disable repo slackhub mention`
    """
    '''
    Disable notifications on a repository for the requesting user.  Preserves settings so they can 
    be disabled at will.
    :param message: message body that holds things like the user and how to reply
    :param target: type of notification to disable
    '''
    slack_id = get_user_id(message)
    repo_config = get_repo_config(slack_id, name)

    try:
        if target == 'all':
            for key in repo_config[2]['enabled'].keys():
                repo_config[2]['enabled'][key] = False
        else:
            repo_config[2]['enabled'][target] = False
    except KeyError:
        pass

    save_user(repo_config[0], slack_id)
    message.reply('Disabled [*' + target + '*] on repo ' + name
                  + '.  Can be re-enabled using: _enable ' + target + '_')


@respond_to('enable (all|label|mention|pr)')
def enable_notifications(message, target):
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
    details = get_user_details(slack_id)

    try:
        if target == 'all':
            for key in details['enabled'].keys():
                details['enabled'][key] = True
        else:
            details['enabled'][target] = True
    except KeyError:
        pass

    save_user(details, slack_id)
    message.reply('Enabled [*' + target + '*].  Can be disabled using: _disable ' + target + '_')


@respond_to('enable repo ([\w-]+) (all|label|maintainer|mention|pr|)')
def enable_repo_notifications(message, name, target):
    """
    Enable notifications on a repo selectively or for all while preserving settings. e.g. `enable mention`
    """
    '''
    Enable notifications on a repository for the requesting user.  Preserves settings so they can be 
    enabled at will.
    :param message: message body that holds things like the user and how to reply
    :param target: type of notification to enable
    '''
    slack_id = get_user_id(message)
    repo_config = get_repo_config(slack_id, name)

    try:
        if target == 'all':
            for key in repo_config[2]['enabled'].keys():
                repo_config[2]['enabled'][key] = True
        else:
            repo_config[2]['enabled'][target] = True
    except KeyError:
        pass

    save_user(repo_config[0], slack_id)
    message.reply('Enabled [*' + target + '*] on repo ' + name
                  + '.  Can be disabled using: _disable ' + target + '_')


@respond_to('username ([\w-]+)$')
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
    details = get_user_details(slack_id)

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


def get_repo_config(slack_id, name):
    """
    Get the repo config of a repository for a user.  This will be a tuple of the user details, 
    the repo list, and the requested repo.
    :param slack_id: user id to get repo config for
    :param name: repository
    :return: tuple of ({details}, [repo], repo); None for positions not found
    """
    details = get_user_details(slack_id)

    try:
        repos = details['repo']

        for repo in repos:
            if repo.get('name') == name:
                return details, repos, repo

        return details, repos, None
    except KeyError:
        pass

    return details, None, None


def get_user_details(slack_id):
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


def get_user_id(message):
    """
    Get the user id from the message body
    :param message: message body to parse
    :return: user id from the message
    """
    return message.user['id']

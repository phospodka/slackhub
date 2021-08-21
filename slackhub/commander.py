from slackhub.persister import list_repos, load_user, save_user, save_admin, list_admins, \
    load_channel, save_channel


def list_channel(slack_id, action):
    try:
        if action == 'all':
            data = load_channel(slack_id)
        else:
            data = load_channel(slack_id)[action]

    except KeyError:
        data = None

    return data


def list_user(slack_id, action):
    try:
        if action == 'all':
            data = load_user(slack_id)
        else:
            data = load_user(slack_id)[action]

    except KeyError:
        data = None

    return data


def add_details(slack_id, details, action, target):
    try:
        my_set = set(details[action])
        my_set.add(target)
        details[action] = list(my_set)
    except KeyError:
        my_set = set()
        my_set.add(target)
        details[action] = list(my_set)

    _save(slack_id, details)


def add_repo(slack_id, repo_config, name):
    # if we did not found the repo, add it
    # else if we did not find a repos list, create it and add the repo
    if not repo_config[2]:
        repo_config[1].append(_create_repo(name))
    elif not repo_config[1]:
        repos = [_create_repo(name)]
        repo_config[0]['repo'] = repos

    _save(slack_id, repo_config[0])


def add_repo_details(slack_id, repo_config, name, action, target):
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
        repo = _create_repo(name)
        my_set = set()
        my_set.add(target)
        repo[action] = list(my_set)
        repo_config[1].append(repo)
    else:
        repo = _create_repo(name)
        my_set = set()
        my_set.add(target)
        repo[action] = list(my_set)
        repos = [repo]
        repo_config[0]['repo'] = repos

    _save(slack_id, repo_config[0])


def remove_details(slack_id, details, action, target):
    try:
        my_set = set(details[action])
        my_set.remove(target)
        details[action] = list(my_set)
    except KeyError:
        pass

    _save(slack_id, details)


def remove_repo(slack_id, repo_config):
    # if we found the repo, remove it
    if repo_config[2]:
        repo_config[1].remove(repo_config[2])

    _save(slack_id, repo_config[0])


def remove_repo_details(slack_id, repo_config, action, target):
    # if the repo was found, remove the requested subscription
    if repo_config[2]:
        try:
            my_set = set(repo_config[2][action])
            my_set.remove(target)
            repo_config[2][action] = list(my_set)
        except KeyError:
            pass

    _save(slack_id, repo_config[0])


def _create_repo(repo):
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


def disable_feature(slack_id, details, target):
    try:
        if target == 'all':
            for key in details['enabled'].keys():
                details['enabled'][key] = False
        else:
            details['enabled'][target] = False
    except KeyError:
        pass

    _save(slack_id, details)


def disable_repo_feature(slack_id, repo_config, target):
    try:
        if target == 'all':
            for key in repo_config[2]['enabled'].keys():
                repo_config[2]['enabled'][key] = False
        else:
            repo_config[2]['enabled'][target] = False
    except KeyError:
        pass

    _save(slack_id, repo_config[0])


def enable_feature(slack_id, details, target):
    try:
        if target == 'all':
            for key in details['enabled'].keys():
                details['enabled'][key] = True
        else:
            details['enabled'][target] = True
    except KeyError:
        pass

    _save(slack_id, details)


def enable_repo_feature(slack_id, repo_config, target):
    try:
        if target == 'all':
            for key in repo_config[2]['enabled'].keys():
                repo_config[2]['enabled'][key] = True
        else:
            repo_config[2]['enabled'][target] = True
    except KeyError:
        pass

    _save(slack_id, repo_config[0])


def save_username(slack_id, details, username):
    try:
        details['username'] = username
    except KeyError:
        pass

    _save(slack_id, details)


def _save(slack_id, details):
    if details.get('type') == 'user':
        save_user(details, slack_id)
    elif details.get('type') == 'channel':
        save_channel(details, slack_id)

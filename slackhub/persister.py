import json
import os
import sys

"""
Handles persisting the various data constructs required by slackhub. 
"""

#todo condense write actions and populate actions into a single method that takes input
#todo make certain methods private (like write and populate)
#todo clean deprecated methods

# cache of the admins in the system
_admins = []

# cache of the channels in the system
_channels = {}

# cache of the repos being maintained
_repos = []

# cache of the users in the system
_users = {}

# directory of the system data
_datadir = os.path.dirname(os.path.realpath(sys.argv[0])) + '/data/'

# directory of the admin data
_admindir = _datadir + 'admins/'

# directory of the channel data
_channeldir = _datadir + 'channels/'

# directory of the repository data
_repodir = _datadir + 'repos/'

# directory of the user data
_userdir = _datadir + 'users/'


def get_cache():
    """
    Get the cache of users
    :return: the dictionary cache users
    """
    if _channels == {}:
        populate_channels()
    if _users == {}:
        populate_users()
    return {**_users, **_channels}  # x | y in 3.9


def load_channel(channel):
    """
    Load the channel from the cache; populate as necessary
    :param channel: channel to load
    :return: channel data as a Python object
    """
    if _channels == {}:
        populate_channels()

    try:
        return _channels[channel]
    except KeyError:
        pass


def list_channels(path):
    """
    internal
    Get the list of channels being maintained by the bot
    :param path: path to search for channels
    :return: list of channel names
    """
    if os.listdir(path):
        return next(os.walk(path))[2]
    else:
        return []


def populate_channels():
    """
    internal
    Walk the persistent file directory and populate the cache
    """
    os.makedirs(_channeldir, exist_ok=True)
    # paths = [os.path.join(path, fn) for fn in next(os.walk(path))[2]]
    names = list_channels(_channeldir)

    for name in names:
        with open(_channeldir + name, 'r') as f:
            for line in f:
                channel = json.loads(line)
                _channels[name] = channel


def save_channel(data, channel):
    """
    Save channel to the cache and to persistent file
    :param data: data to save
    :param channel: channel data belongs to
    """
    if _channels == {}:
        populate_channels()
    _channels[channel] = data
    write_channel_to_file(data, channel)


def write_channel_to_file(data, channel):
    """
    internal
    Write the channel json data out to file
    :param data: data to write
    :param channel: channel to write data for
    """
    with open(_channeldir + channel, 'w') as f:
        f.write(json.dumps(data, sort_keys=True))


def load_user(user):
    """
    Load the user from the cache; populate as necessary
    :param user: username to load
    :return: user data as a Python object
    """
    if _users == {}:
        populate_users()

    try:
        return _users[user]
    except KeyError:
        pass


def load_user_from_file(user):
    """
    deprecated
    Load the user json data from file and return as a Python object structure.
    :param user: username to load
    :return: user data as a Python object
    """
    # open the file for reading if it exist, if it does not we are okay with that
    try:
        with open(_userdir + user, 'r+') as f:
            for line in f:
                if user in line:
                    return json.loads(line)
    except FileNotFoundError:
        pass


def list_users(path):
    """
    internal
    Get the list of users being maintained by the bot
    :param path: path to search for users
    :return: list of usernames
    """
    if os.listdir(path):
        return next(os.walk(path))[2]
    else:
        return []


def populate_users():
    """
    internal
    Walk the persistent file directory and populate the cache
    """
    os.makedirs(_userdir, exist_ok=True)
    # paths = [os.path.join(path, fn) for fn in next(os.walk(path))[2]]
    usernames = list_users(_userdir)

    for username in usernames:
        with open(_userdir + username, 'r') as f:
            for line in f:
                user = json.loads(line)
                _users[username] = user


def save_user(data, user):
    """
    Save user to the cache and to persistent file
    :param data: data to save
    :param user: username data belongs to
    """
    if _users == {}:
        populate_users()
    _users[user] = data
    write_user_to_file(data, user)


def write_user_to_file(data, user):
    """
    internal
    Write the user json data out to file
    :param data: data to write
    :param user: user to write data for
    """
    with open(_userdir + user, 'w') as f:
        f.write(json.dumps(data, sort_keys=True))


def populate_repos():
    """
    internal
    Load the repos from storage into the cache
    """
    os.makedirs(_repodir, exist_ok=True)

    with open(_repodir + 'repos.txt', 'r') as f:
        for repo in f:
            _repos.append(repo.strip())

    _repos.sort()


def save_repo(repo):
    """
    Add a new repository to the system
    :param repo: repository to add
    """
    if not _repos:
        populate_repos()

    write_repo_to_file(repo)
    _repos.append(repo)
    _repos.sort()


def list_repos():
    """
    Get the list of repositories
    :return: the list of repositories
    """
    if not _repos:
        populate_repos()
    return _repos


def write_repo_to_file(data):
    """
    internal
    Add a new repository to the repository file
    :param data: repository to write
    """
    with open(_repodir + 'repos.txt', 'a+') as f:
        f.write(data + '\n')


def populate_admins():
    """
    internal
    Load the admins from storage into the cache
    """
    os.makedirs(_admindir, exist_ok=True)

    with open(_admindir + 'admins.txt', 'r') as f:
        for admin in f:
            _admins.append(admin.strip())

    _admins.sort()


def save_admin(admin):
    """
    Add a new admin to the system
    :param admin: admin to add
    """
    if not _admins:
        populate_admins()

    write_repo_to_file(admin)
    _admins.append(admin)
    _admins.sort()


def list_admins():
    """
    Get the list of admins
    :return: the list of admins
    """
    if not _admins:
        populate_admins()
    return _admins


def write_admin_to_file(data):
    """
    internal
    Add a new admin to the admin file
    :param data: admin to write
    """
    with open(_admindir + 'admins.txt', 'a+') as f:
        f.write(data + '\n')

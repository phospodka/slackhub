import json
import os
import sys

# the all important cache of users; all important.
_cache = {}

# cache of the repos being maintained
_repos = []

# cache of the users in the system
_users = {}

# directory of the system data
_datadir = os.path.dirname(os.path.realpath(sys.argv[0])) + '/data/'

# directory of the repository data
_repodir = _datadir + 'repos/'

# directory of the repository data
_userdir = _datadir + 'users/'


def load_user(user):
    """
    Load the user from the cache; populate as necessary
    :param user: username to load
    :return: user data as a Python object
    """
    if _cache == {}:
        populate_cache()

    try:
        return _cache[user]
    except KeyError:
        pass


def load_user_from_file(user):
    """
    Load the user json data from file and return as a Python object structure.
    :param user: username to load
    :return: user data as a Python object
    """
    # open the file for reading if it exist, if it does not we are okay with that
    try:
        with open(_datadir + user, 'r+') as f:
            for line in f:
                if user in line:
                    return json.loads(line)
    except FileNotFoundError:
        pass


def list_users(path):
    """
    Get the list of users being maintained by the bot
    :param path: path to search for users
    :return: list of usernames
    """
    if os.listdir(path):
        return next(os.walk(path))[2]
    else:
        return []


def get_cache():
    """
    Get the cache of users
    :return: the dictionary cache users
    """
    if _cache == {}:
        populate_cache()
    return _cache


def populate_cache():
    """
    Walk the persistent file directory and populate the cache
    """
    os.makedirs(_datadir, exist_ok=True)
    # paths = [os.path.join(path, fn) for fn in next(os.walk(path))[2]]
    usernames = list_users(_datadir)

    for username in usernames:
        with open(_datadir + username, 'r') as f:
            for line in f:
                user = json.loads(line)
                _cache[username] = user


def save_user(data, user):
    """
    Save user to the cache and to persistent file
    :param data: data to save
    :param user: username data belongs to
    """
    if _cache == {}:
        populate_cache()
    _cache[user] = data
    write_user_to_file(data, user)


def write_user_to_file(data, user):
    """
    Write the user json data out to file
    :param data: data to write
    :param user: user to write data for
    """
    with open(_datadir + user, 'w') as f:
        f.write(json.dumps(data))


def populate_repos():
    """
    Load the repos from storage into the cache
    """
    os.makedirs(_repodir, exist_ok=True)

    with open(_repodir + 'repos.txt', 'a+') as f:
        for repo in f:
            _repos.append(repo.strip())

    _repos.sort()


def add_repo(repo):
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
    Add a new repository to the repository file
    :param data: repository to write
    """
    with open(_repodir + 'repos.txt', 'a+') as f:
        f.write(data + '\n')

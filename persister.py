import json
import os
import sys

# the all important cache of users; all important.
_cache = {}


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
    homedir = os.path.dirname(os.path.realpath(sys.argv[0]))

    # open the file for reading if it exist, if it does not we are okay with that
    try:
        with open(homedir + '/data/' + user, 'r+') as f:
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
    path = os.path.dirname(os.path.realpath(sys.argv[0])) + '/data/'
    os.makedirs(path, exist_ok=True)
    # paths = [os.path.join(path, fn) for fn in next(os.walk(path))[2]]
    usernames = list_users(path)

    for username in usernames:
        with open(path + username, 'r+') as f:
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
    homedir = os.path.dirname(os.path.realpath(sys.argv[0]))
    with open(homedir + '/data/' + user, 'w') as f:
        f.write(json.dumps(data))

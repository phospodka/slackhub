import ast
import os

"""
Collection of some util methods
"""

def get_bool(env_name):
    """
    Util method to get a boolean from the environment variables
    :param env_name: Name of environment variable
    :return: Boolean value of environment variable
    """
    return ast.literal_eval(get_env(env_name))


def get_env(env_name):
    """
    Util method to get a string from the environment variables
    :param env_name: Name of environment variable
    :return: String balue of environment variable
    """
    return os.environ.get(env_name)


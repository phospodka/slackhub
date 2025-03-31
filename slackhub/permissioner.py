from slackhub.persister import list_admins

"""
Permission support primarily to provide decorator for verifying users 
"""


def verify_admin(fun):
    """
    Decorator for admin verification.
    """
    def decorated(*args, **kwargs):
        """
        Perform verification that calling user is an admin. Expects the first argument to
        be a slack message object. If passed will call original function. If failed it will
        use the message object to reply with access denied to the user.
        :param args: non keyword arguments
        :param kwargs: keyword arguments
        :return: original function if permission is verified
        """
        message = args[0]
        if message and is_admin(message):
            return fun(*args, **kwargs)
        else:
            return 'Access denied'
    return decorated


def is_admin(message):
    """
    Check that the user performing the operation is one of the known admins
    :param message: message bogy to parse
    :return: boolean whether user is an admin or not
    """
    if get_user_id(message) in list_admins():
        return True
    else:
        return False


def get_user_id(message):
    """
    Get the user id from the message body
    :param message: message body to parse
    :return: user id from the message
    """
    #return message.user['id']
    return message.get('user')

import re


def respond_to(pattern, flags=0):
    def respond_to_decorator(fun):
        """
        Decorator for message regex pattern matching and argument expansion.
        """
        def wrapper(*args, **kwargs):
            """
            Does the thing
            :param args: non keyword arguments
            :param kwargs: keyword arguments
            :return: original function if permission is verified
            """
            message = args[0]
            text = message.get('text')
            regex = re.compile(pattern, flags)
            match = re.match(regex, text)
            if match:
                groups = match.groups()
                expected_size = regex.groups
                a = args + groups
                return fun(*a, **kwargs)
            else:
                raise Exception(f'Not a match {pattern}')
        return wrapper
    return respond_to_decorator


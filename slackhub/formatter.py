"""
Handles formatting of web hook messages into notification responses.
"""


def github_commit_comment(message, action):
    """
    Formats github commit comment for slack.
    :return: json formatted slack message
    """
    return [{
        'fallback': message.get('comment').get('body'),
        'color': 'C6DAED',
        'text': message.get('comment').get('body'),
        'footer': '<'
                  + message.get('comment').get('html_url')
                  + '|'
                  + 'Comment'
                  + action
                  + 'by '
                  + message.get('comment').get('user').get('login')
                  + ' on line '
                  + str(message.get('comment').get('position'))
                  + ' of '
                  + message.get('comment').get('path')
                  + '>'
    }]


def github_issue_comment(message, action):
    """
    Formats github issue comment for slack.
    :return: json formatted slack message
    """
    return [{
        'fallback': message.get('repository').get('name')
                    + ' Comment'
                    + action
                    + 'by '
                    + message.get('comment').get('user').get('login'),
        'color': 'C4E8B4',
        'pretext': '<'
                   + message.get('repository').get('html_url')
                   + '|['
                   + message.get('repository').get('name')
                   + ']> Comment'
                   + action
                   + 'by <'
                   + message.get('comment').get('user').get('url')
                   + '|'
                   + message.get('comment').get('user').get('login')
                   + '> on pull request <'
                   + message.get('issue').get('html_url')
                   + '|#'
                   + str(message.get('issue').get('number'))
                   + ' '
                   + message.get('issue').get('title')
                   + '>',
        'text': message.get('comment').get('body')
    }]


def github_label(message):
    """
    Format github label assignment for slack.
    :return: json formatted slack message
    """
    return [{
        'fallback': message.get('repository').get('name')
                    + ' Pull request submitted by '
                    + message.get('pull_request').get('user').get('login')
                    + '. #'
                    + str(message.get('pull_request').get('number'))
                    + ' '
                    + message.get('pull_request').get('title'),
        'color': str(message.get('label').get('color')),
        'pretext': '<'
                   + message.get('repository').get('html_url')
                   + '|['
                   + message.get('repository').get('name')
                   + ']> Pull request submitted by <'
                   + message.get('pull_request').get('user').get('url')
                   + '|'
                   + message.get('pull_request').get('user').get('login')
                   + '>',
        'title': '#'
                 + str(message.get('pull_request').get('number'))
                 + ' '
                 + message.get('pull_request').get('title'),
        'title_link': message.get('pull_request').get('html_url'),
        'text': message.get('pull_request').get('body')
    }]


def github_ping(message):
    """
    Formats github ping for slack.
    :return: json formatted slack message
    """
    return [{
        'fallback': 'Link established with ' + message.get('repository').get('full_name'),
        'text': 'Link established with <'
                + message.get('repository').get('html_url')
                + '|'
                + message.get('repository').get('full_name')
                + '>',
        'footer': 'Reactor Online. Sensors Online. Weapons Online. All Systems Nominal.'
    }]


def github_pr(message, action):
    """
    Formats github pull request for slack.
    :return: json formatted slack message
    """
    return [{
        'fallback': message.get('repository').get('name')
                    + ' Pull request'
                    + action
                    + 'by '
                    + message.get('pull_request').get('user').get('login')
                    + '. #'
                    + str(message.get('pull_request').get('number'))
                    + ' '
                    + message.get('pull_request').get('title'),
        'color': '6CC644',
        'pretext': '<'
                   + message.get('repository').get('html_url')
                   + '|['
                   + message.get('repository').get('name')
                   + ']> Pull request'
                   + action
                   + 'by <'
                   + message.get('pull_request').get('user').get('url')
                   + '|'
                   + message.get('pull_request').get('user').get('login')
                   + '>',
        'title': '#'
                 + str(message.get('pull_request').get('number'))
                 + ' '
                 + message.get('pull_request').get('title'),
        'title_link': message.get('pull_request').get('html_url'),
        'text': message.get('pull_request').get('body')  # pdh here
    }]


def github_pr_assign(message):
    """
    Formats github pull request assignment for slack.
    :return: json formatted slack message
    """
    return [{
        'fallback': message.get('repository').get('name')
                    + ' Assigned pull request # '
                    + message.get('pull_request').get('title'),
        'color': '4183C4',
        'text': '<'
                + message.get('repository').get('html_url')
                + '|['
                + message.get('repository').get('name')
                + ']> Assigned pull request <'
                + message.get('pull_request').get('html_url')
                + '|#'
                + str(message.get('pull_request').get('number'))
                + ' '
                + message.get('pull_request').get('title')
                + '>'
    }]


def github_pr_review(message, action):
    """
    Formats github pull request review for slack.
    :return: json formatted slack message
    """
    return [{
        'fallback': message.get('repository').get('name')
                    + ' Review'
                    + action
                    + 'by '
                    + message.get('review').get('user').get('login')
                    + ' on pull request #'
                    + str(message.get('pull_request').get('number'))
                    + ' '
                    + message.get('pull_request').get('title'),
        'color': 'C4E8B4',
        'pretext': '<'
                   + message.get('repository').get('html_url')
                   + '|['
                   + message.get('repository').get('name')
                   + ']> Review'
                   + action
                   + 'by <'
                   + message.get('review').get('user').get('url')
                   + '|'
                   + message.get('review').get('user').get('login')
                   + '> on pull request <'
                   + message.get('pull_request').get('html_url')
                   + '|#'
                   + str(message.get('pull_request').get('number'))
                   + ' '
                   + message.get('pull_request').get('title')
                   + '>',
        'text': message.get('review').get('body')
    }]


def github_pr_review_comment(message, action):
    """
    Formats pull request review comment for slack.
    :return: json formatted slack message
    """
    return [{
        'fallback': message.get('comment').get('body'),
        'color': 'C4E8B4',
        'text': message.get('comment').get('body'),
        'footer': '<'
                  + message.get('comment').get('html_url')
                  + '|'
                  + 'Comment'
                  + action
                  + 'by '
                  + message.get('comment').get('user').get('login')
                  + ' on line '
                  + str(message.get('comment').get('position'))
                  + ' of '
                  + message.get('comment').get('path')
                  + '>'
    }]


def github_pr_review_request(message):
    """
    Formats pull request review assignment for slack.
    :return: json formatted slack message
    """
    return [{
        'fallback': message.get('repository').get('name')
                    + ' Review requested for pull request # '
                    + message.get('pull_request').get('title'),
        'color': '4183C4',
        'text': '<'
                + message.get('repository').get('html_url')
                + '|['
                + message.get('repository').get('name')
                + ']> Review requested for pull request <'
                + message.get('pull_request').get('html_url')
                + '|#'
                + str(message.get('pull_request').get('number'))
                + ' '
                + message.get('pull_request').get('title')
                + '>'
    }]


def github_pr_closed(message):
    return [{
        'fallback': message.get('repository').get('name')
                    + ' Pull request closed by '
                    + message.get('pull_request').get('user').get('login')
                    + '. #'
                    + str(message.get('pull_request').get('number'))
                    + ' '
                    + message.get('pull_request').get('title'),
        'color': '2CBE4E',
        'pretext': '<'
                   + message.get('repository').get('html_url')
                   + '|['
                   + message.get('repository').get('name')
                   + ']> Pull request closed by <'
                   + message.get('pull_request').get('user').get('url')
                   + '|'
                   + message.get('pull_request').get('user').get('login')
                   + '>',
        'title': '#'
                 + str(message.get('pull_request').get('number'))
                 + ' '
                 + message.get('pull_request').get('title'),
        'title_link': message.get('pull_request').get('html_url')
    }]


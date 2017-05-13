import slackhub.persister   # need to fix circular dependency
import slackhub.dispatcher

#from slackhub.dispatcher import post_message
#from slackhub.persister import get_cache

"""
Handles webhook requests.
"""

# needs a sort of plugin architecture like the slackbot


def github_router(event, message):
    """
    Route a Github web hook to the proper processing place.
    :param event: String type of Github event
    :param message: Json message body from web hook
    """
    '''
    known events -> actions:
        pull_request
            labeled
        ping
        commit_comment
            created
            deleted
            edited
        issue_comment
            created
            deleted
            edited
        pull_request_review_comment
            created
            deleted
            edited
        pull_request_review
            submitted
            edited

        want - pr created; all comments created, edited; commit pushed
    '''
    action = message.get('action')
    print(event + " - " + action)
    print(message)
    if event == 'commit_comment':
        pass
    elif event == 'issue_comment':
        if action == 'created':
            _comment_created(message)
    elif event == 'pull_request':
        if action == 'labeled':
            _labeled(message)
    elif event == 'pull_request_review':
        if action == 'submitted':
            _pr_review_submitted(message)
    elif event == 'pull_request_review_comment':
        if action == 'created':
            _pr_review_comment_created(message)


def _comment_created(message):
    """
    Handle processing of pull request / issue comment creation. They are apparently the same in
    Github's eyes.
    :param message: web hook json message from Github
    """
    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']
        mentions = details['mention']

        for m in mentions:
            if m.lower() in message.get('comment').get('body'):
                slackhub.dispatcher.post_message(user, usertype, [{
                    'fallback': "Required plain-text summary of the attachment.",
                    'color': 'C4E8B4',
                    'pretext': '<'
                               + message.get('repository').get('html_url')
                               + '|['
                               + message.get('repository').get('name')
                               + ']> New comment by <'
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
                }])
                break  # only notify once per user


def _labeled(message):
    """
    Handle label processing.  Intended to notify a channel based on a label add
    :param message: web hook json message from Github
    """
    label = message.get('label').get('name')
    print('labeled: ' + label)

    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']
        labels = details['label']

        for l in labels:
            if l.lower() == label:
                slackhub.dispatcher.post_message(user, usertype, [{
                    'fallback': "Required plain-text summary of the attachment.",
                    'color': str(message.get('label').get('color')),
                    'pretext': '<'
                               + message.get('repository').get('html_url')
                               + '|['
                               + message.get('repository').get('name')
                               + ']> ['
                               + label
                               + '] Pull request submitted by <'
                               + message.get('pull_request').get('user').get('url')
                               + '|'
                               + message.get('pull_request').get('user').get('login')
                               + '>',
                    'text': '<'
                            + message.get('pull_request').get('html_url')
                            + '|#'
                            + str(message.get('pull_request').get('number'))
                            + ' '
                            + message.get('pull_request').get('title')
                            + '>'
                }])
                break  # maybe combine all labels matched if we are returning it? or maybe just not say


def _pr_review_submitted(message): # should change
    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']
        mentions = details['mention']

        for m in mentions:
            if m.lower() in message.get('review').get('body'):
                slackhub.dispatcher.post_message(user, usertype, [{
                    'fallback': "Required plain-text summary of the attachment.",
                    'color': 'C4E8B4',
                    'pretext': '<'
                               + message.get('repository').get('html_url')
                               + '|['
                               + message.get('repository').get('name')
                               + ']> Review submitted by <'
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
                }])
                break  # only notify once per user


def _pr_review_comment_created(message):
    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']
        mentions = details['mention']

        for m in mentions:
            if m.lower() in message.get('comment').get('body'):
                slackhub.dispatcher.post_message(user, usertype, [{
                    'fallback': "Required plain-text summary of the attachment.",
                    'color': 'C4E8B4',
                    'text': message.get('comment').get('body'),
                    'footer': '<'
                              + message.get('comment').get('html_url')
                              + '|'
                              + 'Comment by '
                              + message.get('comment').get('user').get('login')
                              + ' on line '
                              + str(message.get('comment').get('position'))
                              + ' of '
                              + message.get('comment').get('path')
                              + '>'
                }])
                break  # only notify once per user
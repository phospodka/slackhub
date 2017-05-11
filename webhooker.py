import slackhub.persister   # need to fix circular dependency
import slackhub.dispatcher

#from slackhub.dispatcher import post_message
#from slackhub.persister import get_cache

"""
Handles webhook requests.
"""

# needs a sort of plugin architecture like the slackbot


def github_router(event, message):
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
    '''
    action = message.get('action')
    print(event + " - " + action)
    print(message)
    if event == 'commit_comment':
        pass
    elif event == 'issue_comment':
        pass
    elif event == 'pull_request':
        if action == 'labeled':
            _labeling(message)
    elif event == 'pull_request_review':
        pass
    elif event == 'pull_request_review_comment':
        pass


def _labeling(message):
    label = message.get('label').get('name')
    print('labeled: ' + label)

    for user, details in slackhub.persister.get_cache().items():
        labels = details['label']
        usertype = details['type']

        for l in labels:
            if l.lower() == label:
                slackhub.dispatcher.post_message(user, usertype, {
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
                            + str(message.get('number'))
                            + ' '
                            + message.get('pull_request').get('title')
                            + '>'
                })
                break  # maybe combine all labels matched if we are returning it? or maybe just not say



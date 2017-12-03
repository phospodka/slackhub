import slackhub.persister  # need to fix circular dependency
import slackhub.dispatcher

# from slackhub.dispatcher import post_message
# from slackhub.persister import get_cache

"""
Handles web hook requests.
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
    # print(event + ' - ' + str(action))
    # print(message)
    if event == 'commit_comment':
        if action == 'created':
            _commit_comment(message)
    elif event == 'issue_comment':
        if action == 'created' or action == 'edited':
            _issue_comment(message)
    elif event == 'ping':
        _ping(message)
    elif event == 'pull_request':
        if action == 'labeled':
            _labeled(message)
        elif action == 'opened' or action == 'edited':
            _pull_request(message)
        elif action == 'review_requested':
            _pr_review_requested(message)
        elif action == 'assigned':
            _pr_assigned(message)
    elif event == 'pull_request_review':
        if action == 'submitted' or action == 'edited':
            _pr_review(message)
    elif event == 'pull_request_review_comment':
        if action == 'created' or action == 'edited':
            _pr_review_comment(message)


def _commit_comment(message):
    """
    Handle processing of commit comments that are outside of reviews.  Does not currently seem to
    be an edited action yet, but keeping it just in case.
    :param message: web hook json message from Github
    """
    action_insert = ' edited ' if message.get('action') == 'edited' else ' '

    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']
        mentions = list(details['mention'])

        if usertype == 'user':
            mentions.append(details['username'])

        for m in mentions:
            if m.lower() in message.get('comment').get('body'):
                slackhub.dispatcher.post_message(user, usertype, [{
                    'fallback': message.get('comment').get('body'),
                    'color': 'C6DAED',
                    'text': message.get('comment').get('body'),
                    'footer': '<'
                              + message.get('comment').get('html_url')
                              + '|'
                              + 'Comment'
                              + action_insert
                              + 'by '
                              + message.get('comment').get('user').get('login')
                              + ' on line '
                              + str(message.get('comment').get('position'))
                              + ' of '
                              + message.get('comment').get('path')
                              + '>'
                }])
                break  # only notify once per user


def _issue_comment(message):
    """
    Handle processing of pull request / issue comment creation. They are apparently the same in
    Github's eyes.
    todo need to test this against issues as well as pul request.  Event though they go through
    the same type there may be some different (at the very least the wording might not want to be
    pull request exactly.
    :param message: web hook json message from Github
    """
    action_insert = ' edited ' if message.get('action') == 'edited' else ' '

    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']
        mentions = list(details['mention'])

        if usertype == 'user':
            mentions.append(details['username'])

        for m in mentions:
            if m.lower() in message.get('comment').get('body'):
                slackhub.dispatcher.post_message(user, usertype, [{
                    'fallback': message.get('repository').get('name')
                                + ' Comment'
                                + action_insert
                                + 'by '
                                + message.get('comment').get('user').get('login'),
                    'color': 'C4E8B4',
                    'pretext': '<'
                               + message.get('repository').get('html_url')
                               + '|['
                               + message.get('repository').get('name')
                               + ']> Comment'
                               + action_insert
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
                }])
                break  # only notify once per user


def _labeled(message):
    """
    Handle label processing.  Intended to notify a channel based on a label add
    :param message: web hook json message from Github
    """
    label = message.get('label').get('name')
    # print('labeled: ' + label)

    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']
        labels = details['label']

        for l in labels:
            if l.lower() == label:
                slackhub.dispatcher.post_message(user, usertype, [{
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
                }])
                break  # combine all labels matched if we are returning it? or maybe just not say?


def _ping(message):
    """
    Handle ping processing.
    :param message: web hook json message from Github
    """
    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']

        if usertype == 'channel':
            slackhub.dispatcher.post_message(user, usertype, [{
                'fallback': 'Link established with ' + message.get('repository').get('full_name'),
                'text': 'Link established with <'
                        + message.get('repository').get('html_url')
                        + '|'
                        + message.get('repository').get('full_name')
                        + '>',
                'footer': 'Reactor Online. Sensors Online. Weapons Online. All Systems Nominal.'
            }])


def _pull_request(message):
    """
    Handle pull request processing.  Specifically for actions other than labelling.
    :param message: web hook json message from Github
    """
    action_insert = ' edited ' if message.get('action') == 'edited' else ' submitted '

    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']
        mentions = list(details['mention'])

        if usertype == 'user':
            mentions.append(details['username'])

        for m in mentions:
            if m.lower() in message.get('pull_request').get('body'):
                slackhub.dispatcher.post_message(user, usertype, [{
                    'fallback': message.get('repository').get('name')
                                + ' Pull request'
                                + action_insert
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
                               + action_insert
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
                    'text': message.get('pull_request').get('body')
                }])
                break  # only notify once per user


def _pr_assigned(message):
    """
    Handle processing of pull request assigned actions.
    :param message: web hook json message from Github
    """
    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']

        if usertype == 'user':
            enabled = details['enabled']['pr']
            username = details['username']

            if enabled and username.lower() == message.get('assignee').get('login').lower():
                slackhub.dispatcher.post_message(user, usertype, [{
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
                }])


def _pr_review(message):
    """
    Handle processing of pull request review submissions.  This would be the summary text a user
    provides just before submitting.
    :param message: web hook json message from Github
    """
    action_insert = ' edited ' if message.get('action') == 'edited' else ' submitted '

    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']
        mentions = list(details['mention'])

        if usertype == 'user':
            mentions.append(details['username'])

        for m in mentions:
            if m.lower() in message.get('review').get('body'):
                slackhub.dispatcher.post_message(user, usertype, [{
                    'fallback': message.get('repository').get('name')
                                + ' Review'
                                + action_insert
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
                               + action_insert
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
                }])
                break  # only notify once per user


def _pr_review_comment(message):
    """
    Handle processing of pull request review comments.
    :param message: web hook json message from Github
    """
    action_insert = ' edited ' if message.get('action') == 'edited' else ' '

    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']
        mentions = list(details['mention'])

        if usertype == 'user':
            mentions.append(details['username'])

        for m in mentions:
            if m.lower() in message.get('comment').get('body'):
                slackhub.dispatcher.post_message(user, usertype, [{
                    'fallback': message.get('comment').get('body'),
                    'color': 'C4E8B4',
                    'text': message.get('comment').get('body'),
                    'footer': '<'
                              + message.get('comment').get('html_url')
                              + '|'
                              + 'Comment'
                              + action_insert
                              + 'by '
                              + message.get('comment').get('user').get('login')
                              + ' on line '
                              + str(message.get('comment').get('position'))
                              + ' of '
                              + message.get('comment').get('path')
                              + '>'
                }])
                break  # only notify once per user


def _pr_review_requested(message):
    """
    Handle processing of pull request review request actions.
    :param message: web hook json message from Github
    """
    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']

        if usertype == 'user':
            enabled = details['enabled']['pr']
            username = details['username']

            if enabled \
                    and username.lower() == message.get('requested_reviewer').get('login').lower():
                slackhub.dispatcher.post_message(user, usertype, [{
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
                }])

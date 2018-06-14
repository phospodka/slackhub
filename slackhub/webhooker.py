import slackhub.persister  # need to fix circular dependency
import slackhub.dispatcher
import slackhub.formatter

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
        if action == 'submitted':  # or action == 'edited':  # leaving this off for now since a review sends both
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
    action = ' edited ' if message.get('action') == 'edited' else ' '

    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']
        mentions = list(details['mention'])

        if usertype == 'user':
            mentions.append(details['username'])

        for m in mentions:
            body = message.get('comment').get('body')
            if body is not None and m.lower() in body:
                slackhub.dispatcher.post_message(user, usertype,
                        slackhub.formatter.github_commit_comment(message, action))
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
    action = ' edited ' if message.get('action') == 'edited' else ' '

    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']
        mentions = list(details['mention'])

        if usertype == 'user':
            mentions.append(details['username'])

        for m in mentions:
            body = message.get('comment').get('body')
            if body is not None and m.lower() in body:
                slackhub.dispatcher.post_message(user, usertype,
                        slackhub.formatter.github_issue_comment(message, action))
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
                slackhub.dispatcher.post_message(user, usertype,
                        slackhub.formatter.github_label(message))
                break  # combine all labels matched if we are returning it? or maybe just not say?


def _ping(message):
    """
    Handle ping processing.
    :param message: web hook json message from Github
    """
    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']

        if usertype == 'channel':
            slackhub.dispatcher.post_message(user, usertype,
                    slackhub.formatter.github_ping(message))


def _pull_request(message):
    """
    Handle pull request processing.  Specifically for actions other than labelling.
    :param message: web hook json message from Github
    """
    action = ' edited ' if message.get('action') == 'edited' else ' submitted '

    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']
        mentions = list(details['mention'])

        if usertype == 'user':
            mentions.append(details['username'])

        for m in mentions:
            body = message.get('pull_request').get('body')
            if body is not None and m.lower() in body:
                slackhub.dispatcher.post_message(user, usertype,
                        slackhub.formatter.github_pr(message, action))
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
                slackhub.dispatcher.post_message(user, usertype,
                        slackhub.formatter.github_pr_assign(message))


def _pr_review(message):
    """
    Handle processing of pull request review submissions.  This would be the summary text a user
    provides just before submitting.
    :param message: web hook json message from Github
    """
    action = ' edited ' if message.get('action') == 'edited' else ' submitted '

    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']
        mentions = list(details['mention'])

        if usertype == 'user':
            mentions.append(details['username'])

        for m in mentions:
            body = message.get('review').get('body')
            if body is not None and m.lower() in body:
                slackhub.dispatcher.post_message(user, usertype,
                        slackhub.formatter.github_pr_review(message, action))
                break  # only notify once per user


def _pr_review_comment(message):
    """
    Handle processing of pull request review comments.
    :param message: web hook json message from Github
    """
    action = ' edited ' if message.get('action') == 'edited' else ' '

    for user, details in slackhub.persister.get_cache().items():
        usertype = details['type']
        mentions = list(details['mention'])

        if usertype == 'user':
            mentions.append(details['username'])

        for m in mentions:
            body = message.get('comment').get('body')
            if body is not None and m.lower() in body:
                slackhub.dispatcher.post_message(user, usertype,
                        slackhub.formatter.github_pr_review_comment(message, action))
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
                slackhub.dispatcher.post_message(user, usertype,
                        slackhub.formatter.github_pr_review_request(message))

import logging
import unicodedata

import slackhub.dispatcher as dispatcher
import slackhub.formatter as formatter
import slackhub.persister as persister # need to fix circular dependency

# from slackhub.dispatcher import post_message
# from slackhub.persister import get_cache

"""
Handles web hook requests.
"""

# todo needs a sort of plugin architecture like the slackbot

logger = logging.getLogger(__name__)


def github_router(event, message):
    """
    Route a Github web hook to the proper processing place.
    :param event: String type of Github event
    :param message: Json message body from web hook
    """
    '''
    known events -> actions:
        pull_request
            closed
            labeled
            opened
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
    logger.debug('%s(%s) - %s', event, action, message)

    if event == 'commit_comment':
        if action == 'created':
            _commit_comment(message)
    elif event == 'gollum':
        # _wiki(message)
        pass
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
        elif action == 'closed':  # ? pdh test this
            # _pr_closed(message)
            pass
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

    for user, details in persister.get_cache().items():
        body = message.get('comment').get('body')
        repo = message.get('repository').get('name')
        if _is_global_mentioned(details, body) or _is_repo_mentioned(details, repo, body):
            dispatcher.post_message(user, formatter.github_commit_comment(message, action))


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

    for user, details in persister.get_cache().items():
        body = message.get('comment').get('body')
        repo = message.get('repository').get('name')
        if _is_global_mentioned(details, body) or _is_repo_mentioned(details, repo, body):
            dispatcher.post_message(user, formatter.github_issue_comment(message, action))


def _labeled(message):
    """
    Handle label processing.  Intended to notify a channel based on a label add
    :param message: web hook json message from Github
    """
    label = message.get('label').get('name')

    for user, details in persister.get_cache().items():
        enabled = details['enabled']['label']
        labels = details['label']

        if enabled:
            for l in labels:
                if l.lower() == label:
                    dispatcher.post_message(user, formatter.github_label(message))
                    break  # combine all labels matched if we are returning it? or maybe just not say?


def _ping(message):
    """
    Handle ping processing.
    :param message: web hook json message from Github
    """
    is_repo = message.get('repository')
    is_org = message.get('organization')

    if is_repo:
        persister.save_repo(message.get('repository').get('name'))

    for user, details in persister.get_cache().items():
        usertype = details['type']

        if usertype == 'channel':
            if is_repo:
                dispatcher.post_message(user, formatter.github_ping_repo(message))
            elif is_org:
                dispatcher.post_message(user, formatter.github_ping_org(message))


def _pull_request(message):
    """
    Handle pull request processing.  Specifically for actions other than labelling.
    :param message: web hook json message from Github
    """
    action = ' edited ' if message.get('action') == 'edited' else ' submitted '

    for user, details in persister.get_cache().items():
        body = message.get('pull_request').get('body')
        repo = message.get('repository').get('name')
        if _is_maintainer(details, repo) \
                or _is_global_mentioned(details, body) \
                or _is_repo_mentioned(details, repo, body):
            dispatcher.post_message(user, formatter.github_pr(message, action))


def _pr_closed(message):
    """
    Handle processing of pull request closed actions.
    :param message: web hook json message from Github
    """
    for user, details in persister.get_cache().items():
        usertype = details['type']

        if usertype == 'channel':
            if details['operation']['closed']:
                dispatcher.post_message(user, formatter.github_pr_closed(message))


def _pr_assigned(message):
    """
    Handle processing of pull request assigned actions.
    :param message: web hook json message from Github
    """
    for user, details in persister.get_cache().items():
        usertype = details['type']

        if usertype == 'user':
            enabled = details['enabled']['pr']
            username = details['username']

            if enabled and _caseless_equals(username, message.get('assignee').get('login')):
                dispatcher.post_message(user, formatter.github_pr_assign(message))


def _pr_review(message):
    """
    Handle processing of pull request review submissions.  This would be the summary text a user
    provides just before submitting.
    :param message: web hook json message from Github
    """
    action = ' edited ' if message.get('action') == 'edited' else ' submitted '

    for user, details in persister.get_cache().items():
        body = message.get('review').get('body')
        repo = message.get('repository').get('name')
        if _is_global_mentioned(details, body) or _is_repo_mentioned(details, repo, body):
            dispatcher.post_message(user, formatter.github_pr_review(message, action))


def _pr_review_comment(message):
    """
    Handle processing of pull request review comments.
    :param message: web hook json message from Github
    """
    action = ' edited ' if message.get('action') == 'edited' else ' '

    for user, details in persister.get_cache().items():
        body = message.get('comment').get('body')
        repo = message.get('repository').get('name')
        if _is_global_mentioned(details, body) or _is_repo_mentioned(details, repo, body):
            dispatcher.post_message(user, formatter.github_pr_review_comment(message, action))


def _pr_review_requested(message):
    """
    Handle processing of pull request review request actions.
    :param message: web hook json message from Github
    """
    for user, details in persister.get_cache().items():
        usertype = details['type']

        if usertype == 'user':
            enabled = details['enabled']['pr']
            username = details['username']

            if enabled \
                    and _caseless_equals(username, message.get('requested_reviewer').get('login')):
                dispatcher.post_message(user, formatter.github_pr_review_request(message))


def _wiki(message):
    for user, details in persister.get_cache().items():
        target_repo = message.get('repository').get('name')
        if _is_maintainer(details, target_repo):
            dispatcher.post_message(user, formatter.github_wiki(message))


def _is_global_mentioned(details, body):
    """
    Perform the check if a global mention is matched
    :param details: details to get configured mentions from
    :param body: message body to check for mentions in
    :return: boolean whether a mention was found
    """
    enabled = details['enabled']['mention']
    mentions = list(details['mention'])
    usertype = details['type']

    if usertype == 'user':
        mentions.append(details['username'])

    return enabled and _is_mentioned(mentions, body)


def _is_repo_mentioned(details, target_repo, body):
    """
    Perform the check if a global mention is matched
    :param details: details to get configured mentions from
    :param target_repo: repo to check for configuration in
    :param body: message body to check for mentions in
    :return: boolean whether a mention was found
    """
    repos = details['repo']

    for repo in repos:
        if _is_repo_match(repo, target_repo):
            enabled = repo['enabled']['mention']
            mentions = list(repo['mention'])
            usertype = details['type']

            if usertype == 'user':
                mentions.append(details['username'])

            return enabled and _is_mentioned(mentions, body)

    # if we found nothing return false
    return False


def _is_maintainer(details, target_repo):
    """
    Perform the check if the user is a maintainer of the repo
    :param details: details of the user to find repo match
    :param target_repo: repo to check for maintainer flag in
    :return: boolean whether the user is a maintainer
    """
    repos = details['repo']

    for repo in repos:
        if _is_repo_match(repo, target_repo):
            return repo['enabled']['maintainer']

    # if we found nothing return false
    return False


def _is_mentioned(mentions, body):
    """
    Check the mentions list to see if there is a match in the message body.
    :param mentions: mentions list to iterate through
    :param body: message body to for for match in.
    :return: boolean whether a mention was matched
    """
    for m in mentions:
        if _caseless_contains(m, body):
            return True
    return False


def _is_repo_match(repo, target_repo):
    """
    Check if the repo details is a match for a target repo from a message
    :param repo: repo config to get match parameters for
    :param target_repo: repo to check that we match
    :return: boolean whether repo matches the target repo
    """
    repo_name = repo['name']
    prefix = repo['enabled']['prefix']
    if prefix:
        return target_repo.startswith(repo_name)
    else:
        return repo_name == target_repo


def _normalize(text):
    """
    Casefold the unicode text to allow for caseless comparison and normalize prevent variations of
    accents on letters from mis-matching.
    :param text: input text to normalize
    :return: normalized text
    """
    return unicodedata.normalize("NFKD", text.casefold())


def _caseless_contains(target, source):
    """
    Perform a normalized, case insensitive check of whether a target string is contained in a
    source string.
    :param target: target string we are looking for
    :param source: source string we are looking in
    :return: whether the target string is contained in the source string
    """
    return source is not None and _normalize(target) in _normalize(source)


def _caseless_equals(left, right):
    """
    Perform a normalized, case insensitive equality check
    :param left: left side of the equals operation
    :param right: right side of the equals operation
    :return: whether the two strings are caselessly equal
    """
    return _normalize(left) == _normalize(right)

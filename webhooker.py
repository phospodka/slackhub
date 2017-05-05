import json
import os
import sys

from slackbot import settings

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
    print(event)
    print(message)
    pass

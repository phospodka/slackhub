import re

from slackbot.bot import respond_to

from slackhub.permissioner import is_admin

"""
Handles help docs for users
"""


@respond_to('help', re.IGNORECASE)
def help_me(message):
    """
    Provide list of available commands
    :param message: message body that holds things like the user and how to reply
    """
    if is_admin(message):
        message.reply(_admin_commands() + _user_commands())
    else:
        message.reply(_user_commands())


def _admin_commands():
    return ('*Admin commands*\n'
            + '* `add admin (.*)`'
            + ' - Add user by slack id to the list of admins. e.g. `add admin U056789`\n'
            + '* `add channel ([\\w-]+) (label|mention) (.+)`'
            + ' - Add subscriptions of a label, or mention to a channel. e.g. `add channel C012345 mention username`\n'
            + '* `add channel ([\\w-]+) repo ([\\w-]+) (label|mention) (.+)`'
            + ' - Add subscriptions of a label, or mention to a repository. e.g. `add channel C012345 repo slackhub mention username`\n'
            + '* `add channel ([\\w-]+) repo ([\\w-]+)$`'
            + ' - Add subscription to a repository. e.g. `add channel C012345 repo slackhub`\n'
            + '* `disable channel ([\\w-]+) (all|label|mention|pr)`'
            + ' - Disable notifications selectively or for all while preserving settings. e.g. `disable channel C012345 mention`\n'
            + '* `disable channel ([\\w-]+) repo ([\\w-]+) (all|label|maintainer|mention|pr)`'
            + ' - Disable notifications on a repo selectively or for all while preserving settings. e.g. `disable channel C012345 repo slackhub mention`\n'
            + '* `enable channel ([\\w-]+) (all|label|mention|pr)`'
            + ' - Enable notifications selectively or for all while preserving settings. e.g. `enable channel C012345 mention`\n'
            + '* `enable channel ([\\w-]+) repo ([\\w-]+) (all|label|maintainer|mention|pr)`'
            + ' - Enable notifications on a repo selectively or for all while preserving settings. e.g. `enable channel C012345 mention`\n'
            + '* `init`'
            + ' - if all admins have been removed `init` can be ran to add the first admin'
            + '* `list channel ([\\w-]+) (all|enabled|label|mention|repo|username)`'
            + ' - List stored details for a channel. e.g. `list channel C012345 all`\n'
            + '* `remove admin (.*)`'
            + ' - Remove user by slack id from the list of admins. e.g. `remove admin U056789`\n'
            + '* `remove channel ([\\w-]+) (label|mention) (.+)`'
            + ' - Remove subscriptions of a label, or mention to a channel. e.g. `remove channel C012345 mention username`\n'
            + '* `remove channel ([\\w-]+) repo ([\\w-]+) (label|mention) (.+)`'
            + ' - Remove subscriptions of a label, or mention from a repository. e.g. `remove channel C012345 repo slackhub mention username`\n'
            + '* `remove channel ([\\w-]+) repo ([\\w-]+)$`'
            + ' - Remove subscription to a repository. e.g. `remove channel C012345 repo slackhub`\n')


def _user_commands():
    return ('*User commands*\n'
            + '* `add (label|mention) (.+)`'
            + ' - Add subscriptions of a label, or mention. e.g. `add mention username`\n'
            + '* `add repo ([\\w-]+) (label|mention) (.+)`'
            + ' - Add subscriptions of a label, or mention to a repository. e.g. `add repo slackhub mention username`\n'
            + '* `add repo ([\\w-]+)$`'
            + ' - Add subscription to a repository. e.g. `add repo slackhub`\n'
            + '* `disable (all|label|mention|pr)`'
            + ' - Disable notifications selectively or for all while preserving settings. e.g. `disable mention`\n'
            + '* `disable repo ([\\w-]+) (all|label|maintainer|mention|pr)`'
            + ' - Disable notifications on a repo selectively or for all while preserving settings. e.g. `disable repo slackhub mention`\n'
            + '* `enable (all|label|mention|pr)`'
            + ' - Enable notifications selectively or for all while preserving settings. e.g. `enable mention`\n'
            + '* `enable repo ([\\w-]+) (all|label|maintainer|mention|pr)`'
            + ' - Enable notifications on a repo selectively or for all while preserving settings. e.g. `enable mention`\n'
            + '* `list admin`'
            + ' - List current admins. e.g. `list admin`\n'
            + '* `list (all|enabled|label|mention|repo|username)`'
            + ' - List stored details for a user. e.g. `list mention`\n'
            + '* `remove (label|mention) (.+)`'
            + ' - Remove subscriptions of a label, or mention. e.g. `remove mention username`\n'
            + '* `remove repo ([\\w-]+) (label|mention) (.+)`'
            + ' - Remove subscriptions of a label, or mention from a repository. e.g. `remove repo slackhub mention username`\n'
            + '* `remove repo ([\\w-]+)$`'
            + ' - Remove subscription to a repository. e.g. `remove repo slackhub`\n'
            + '* `repos`'
            + ' - List the repositories being watched\n'
            + '* `username ([\\w-]+)$`'
            + ' - Set your github username to links notifications to this slack account. e.g. `username batman`\n')

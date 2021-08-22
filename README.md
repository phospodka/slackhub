Slackhub
========================

Slackhub is a Github integration for slack that aims to provide direct notification for keyword 
matching, label application, and repository updates.  This is done by messaging the bot commands to 
manage subscriptions.  Admin users can be setup to allow for creating similar subscriptions to
channels.  

Dependencies
------------------------

Relies on [slacker](https://github.com/os/slacker), [slackbot](https://github.com/lins05/slackbot), and
[flask](https://github.com/pallets/flask) Python projects.

Install the main requirements with:

`pip install -r requirements.txt`

Everything is tested using Python version 3.5

Getting started
------------------------

After downloading and installing the requirements you will want to edit a couple of the config items in **slackbot_settings.py**.
* API_TOKEN - create a bot in slack and generate a token to use here.  This is what allows the bot to communicate with slack.
* BOT_NAME - set the name of the bot you created in slack here.  This allows this code to send notifications to the bot.
* SLACKHUB_TOKEN - set this to your favorite random string.  This will be used as part of the URL for the webhook sink for github.

With all the settings set, run the main program **slackhubbot.py** with either:
* `python slackhubbot.py`
* `nohup python slackhubbot.py &`

When starting, it is important to either run the command from the directory that **slackhubbot.py** is in, or to add the folder where
it is checked out to the PATH variable.  i.e. `PATH=$PATH:/slackhub`.  This is because starting this is still somewhat hacky with 
getting the dependencies in place.

Slackhub will create a **/data** directory in the checkout folder.  This is where individuals files per user will be created to
store their settings.  It should create it for you, but will want to make sure the user you start this with has permissions to
create the folder and the files in it.

If all has gone well, you should see some output that looks like:

```
[DD/MM/YYYY 00:00:00] slackd : INFO - Initializing slackbot
[DD/MM/YYYY 00:00:00] webhookd : INFO - Initializing flask
[DD/MM/YYYY 00:00:00] slackbot.manager : slackd : INFO - loading plugin "slackhub"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "help_me" to "help"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "decorated" to "add admin (.*)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "list_admin" to "list admin"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "decorated" to "list channel ([\w-]+) (all|enabled|label|mention|repo|username)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "decorated" to "add channel ([\w-]+) (label|mention) (.+)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "decorated" to "add channel ([\w-]+) repo ([\w-]+) (label|mention) (.+)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "decorated" to "add channel ([\w-]+) repo ([\w-]+)$"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "decorated" to "remove channel ([\w-]+) (label|mention) (.+)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "decorated" to "remove channel ([\w-]+) repo ([\w-]+) (label|mention) (.+)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "decorated" to "remove channel ([\w-]+) repo ([\w-]+)$"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "decorated" to "disable channel ([\w-]+) (all|label|mention|pr)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "decorated" to "disable channel ([\w-]+) repo ([\w-]+) (all|label|maintainer|mention|pr)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "decorated" to "enable channel ([\w-]+) (all|label|mention|pr)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "decorated" to "enable channel ([\w-]+) repo ([\w-]+) (all|label|maintainer|mention|pr)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "list_actions" to "list (all|enabled|label|mention|repo|username)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "add_actions" to "add (label|mention) (.+)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "add_repo_actions" to "add repo ([\w-]+) (label|mention) (.+)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "add_repos" to "add repo ([\w-]+)$"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "remove_actions" to "remove (label|mention) (.+)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "remove_repo_actions" to "remove repo ([\w-]+) (label|mention) (.+)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "remove_repos" to "remove repo ([\w-]+)$"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "disable_notifications" to "disable (all|label|mention|pr)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "disable_repo_notifications" to "disable repo ([\w-]+) (all|label|maintainer|mention|pr)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "enable_notifications" to "enable (all|label|mention|pr)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "enable_repo_notifications" to "enable repo ([\w-]+) (all|label|maintainer|mention|pr)"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "set_username" to "username ([\w-]+)$"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - registered respond_to plugin "list_repositories" to "repos"
[DD/MM/YYYY 00:00:00] slackbot.bot : slackd : INFO - connected to slack RTM api
[DD/MM/YYYY 00:00:00] slackbot.bot : Dummy-1 : INFO - keep active thread started
```

Usage
------------------------

The important commands are:

**Admin Commands**
* `add admin (.*)` - Add user to the list of admins. e.g. add admin username
* `add channel ([\w-]+) (label|mention) (.+)` - Add subscriptions of a label, or mention to a channel. e.g. add channel C012345 mention username
* `add channel ([\w-]+) repo ([\w-]+) (label|mention) (.+)` - Add subscriptions of a label, or mention to a repository. e.g. add channel C012345 repo slackhub mention username
* `add channel ([\w-]+) repo ([\w-]+)$` - Add subscription to a repository. e.g. add channel C012345 repo slackhub
* `disable channel ([\w-]+) (all|label|mention|pr)` - Disable notifications selectively or for all while preserving settings. e.g. disable channel C012345 mention
* `disable channel ([\w-]+) repo ([\w-]+) (all|label|maintainer|mention|pr)` - Disable notifications on a repo selectively or for all while preserving settings. e.g. disable channel C012345 repo slackhub mention
* `enable channel ([\w-]+) (all|label|mention|pr)` - Enable notifications selectively or for all while preserving settings. e.g. enable channel C012345 mention
* `enable channel ([\w-]+) repo ([\w-]+) (all|label|maintainer|mention|pr)` - Enable notifications on a repo selectively or for all while preserving settings. e.g. enable channel C012345 mention
* `list channel ([\w-]+) (all|enabled|label|mention|repo|username)` - List stored details for a channel. e.g. list channel C012345 all
* `remove channel ([\w-]+) (label|mention) (.+)` - Remove subscriptions of a label, or mention to a channel. e.g. remove channel C012345 mention username
* `remove channel ([\w-]+) repo ([\w-]+) (label|mention) (.+)` - Remove subscriptions of a label, or mention from a repository. e.g. remove channel C012345 repo slackhub mention username
* `remove channel ([\w-]+) repo ([\w-]+)$` - Remove subscription to a repository. e.g. remove channel C012345 repo slackhub

**User Commands**
* `add (label|mention) (.+)` - Add subscriptions of a label, or mention. e.g. add mention username
* `add repo ([\w-]+) (label|mention) (.+)` - Add subscriptions of a label, or mention to a repository. e.g. add repo slackhub mention username
* `add repo ([\w-]+)$` - Add subscription to a repository. e.g. add repo slackhub
* `disable (all|label|mention|pr)` - Disable notifications selectively or for all while preserving settings. e.g. disable mention
* `disable repo ([\w-]+) (all|label|maintainer|mention|pr)` - Disable notifications on a repo selectively or for all while preserving settings. e.g. disable repo slackhub mention
* `enable (all|label|mention|pr)` - Enable notifications selectively or for all while preserving settings. e.g. enable mention
* `enable repo ([\w-]+) (all|label|maintainer|mention|pr)` - Enable notifications on a repo selectively or for all while preserving settings. e.g. enable mention
* `list admin` - List current admins. e.g. list admin
* `list (all|enabled|label|mention|repo|username)` - List stored details for a user. e.g. list mention
* `remove (label|mention) (.+)` - Remove subscriptions of a label, or mention. e.g. remove mention username
* `remove repo ([\w-]+) (label|mention) (.+)` - Remove subscriptions of a label, or mention from a repository. e.g. remove repo slackhub mention username
* `remove repo ([\w-]+)$` - Remove subscription to a repository. e.g. remove repo slackhub
* `repos` - List the repositories being watched
* `username ([\w-]+)$` - Set your github username to links notifications to this slack account. e.g. username batman


License
-------------------------------

See LICENSE file.  MPL 2.0.

Plan
-------------------------

There are a number of items I'd like to do.

* add better logging
* tests ;_;
* figure out how to make this installable
* move github messages to templates
* provide docker container
* convert from bot to app in slack
* provide wiki

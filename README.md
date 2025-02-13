Slackhub
========================

Slackhub is a Github integration for slack that aims to provide direct notification for keyword 
matching, label application, and repository updates.  This is done by messaging the bot commands to 
manage subscriptions.  Admin users can be setup to allow for creating similar subscriptions to
channels.  

Dependencies
------------------------

Relies on [slack-bolt](https://github.com/slackapi/bolt-python), [slack-sdk](https://github.com/slackapi/python-slack-sdk), and
[flask](https://github.com/pallets/flask) Python projects.

Install the main requirements with:

`pip install -r requirements.txt`

Add slackhub to your path:

`export PYTHONPATH=$PYTHONPATH:/path/to/slackhub`

Everything is tested using Python version 3.12

Getting started
------------------------

Before running you will want to create a `.env` file
```python
DEBUG = True  # flag to globally enable debug logging  
DEFAULT_REPLY = "Heyo!  Please type `help` for a list of commands."
SLACK_APP_TOKEN = 'app_token'  # app token for this slack app 
SLACK_BOT_TOKEN = 'bot_token'  # bot user token for this app for your workspace
SLACKHUB_TOKEN = '12345B'  # token to use as part of the url for web hooks
WEBHOOK_ENABLED = True   # flag to enable the webhook accepting events
```
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
[DD/MM/YYYY 00:00:00] __main__ : slackd : INFO - Initializing slackbot
[DD/MM/YYYY 00:00:00] __main__ : webhookd : INFO - Initializing flask
 * Serving Flask app 'slackhubbot'
 * Debug mode: off
[DD/MM/YYYY 00:00:00] slack_bolt.App : slackd : INFO - A new session has been established (session id: 10011001-2222-3333-4444-556677889900)
[DD/MM/YYYY 00:00:00] slack_bolt.App : slackd : INFO - ⚡️ Bolt app is running!
[DD/MM/YYYY 00:00:00] slack_bolt.App : Thread-1 (_run) : INFO - Starting to receive messages from a new connection (session id: 10011001-2222-3333-4444-556677889900)
```

Usage
------------------------

The important commands are:

**Setup Commands**
* `init`

**Admin Commands**
* `add admin (.*)`
* `add channel ([\w-]+) (label|mention) (.+)`
* `add channel ([\w-]+) repo ([\w-]+) (label|mention) (.+)`
* `add channel ([\w-]+) repo ([\w-]+)$`
* `disable channel ([\w-]+) (all|label|mention|pr)`
* `disable channel ([\w-]+) repo ([\w-]+) (all|label|maintainer|mention|pr)`
* `enable channel ([\w-]+) (all|label|mention|pr)`
* `enable channel ([\w-]+) repo ([\w-]+) (all|label|maintainer|mention|pr)`
* `list channel ([\w-]+) (all|enabled|label|mention|repo|username)`
* `remove admin (.*)`
* `remove channel ([\w-]+) (label|mention) (.+)`
* `remove channel ([\w-]+) repo ([\w-]+) (label|mention) (.+)`
* `remove channel ([\w-]+) repo ([\w-]+)$`

**User Commands**
* `add (label|mention) (.+)`
* `add repo ([\w-]+) (label|mention) (.+)`
* `add repo ([\w-]+)$`
* `disable (all|label|mention|pr)`
* `disable repo ([\w-]+) (all|label|maintainer|mention|pr)`
* `enable (all|label|mention|pr)`
* `enable repo ([\w-]+) (all|label|maintainer|mention|pr)`
* `list admin`
* `list (all|enabled|label|mention|repo|username)`
* `remove (label|mention) (.+)`
* `remove repo ([\w-]+) (label|mention) (.+)`
* `remove repo ([\w-]+)$`
* `repos`
* `username ([\w-]+)$`


License
-------------------------------

See LICENSE file.  MPL 2.0.

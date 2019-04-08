Slackhub
========================

Slackhub is a Github integration for slack that aims to provide direct notification for keyword matching and branch
updates.  This is done by messaging the bot commands to manage subscriptions to keywords or full branch names.  

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
[DD/MM/YYYY 00:00:00] slackd : INFO - loading plugin "slackhub"
[DD/MM/YYYY 00:00:00] slackd : INFO - registered respond_to plugin "add_admin" to "add admin (.*)"
[DD/MM/YYYY 00:00:00] slackd : INFO - registered respond_to plugin "list_admin" to "list admins"
[DD/MM/YYYY 00:00:00] slackd : INFO - registered respond_to plugin "list_actions" to "list (all|enabled|label|mention|repo|username)"
[DD/MM/YYYY 00:00:00] slackd : INFO - registered respond_to plugin "add_actions" to "add (repo )?(label|mention) (.*)"
[DD/MM/YYYY 00:00:00] slackd : INFO - registered respond_to plugin "add_repo" to "add repo (.*)"
[DD/MM/YYYY 00:00:00] slackd : INFO - registered respond_to plugin "remove_actions" to "remove (repo )?(label|mention) (.*)"
[DD/MM/YYYY 00:00:00] slackd : INFO - registered respond_to plugin "remove_repo" to "remove repo (.*)"
[DD/MM/YYYY 00:00:00] slackd : INFO - registered respond_to plugin "disable_notifications" to "disable (repo )?(all|label|maintainer|mention|pr)"
[DD/MM/YYYY 00:00:00] slackd : INFO - registered respond_to plugin "enable_notifications" to "enable (repo )?(all|label|maintainer|mention|pr|)"
[DD/MM/YYYY 00:00:00] slackd : INFO - registered respond_to plugin "set_username" to "username (.*)"
[DD/MM/YYYY 00:00:00] slackd : INFO - registered respond_to plugin "list_repositories" to "repos"
[DD/MM/YYYY 00:00:00] slackd : INFO - connected to slack RTM api
[DD/MM/YYYY 00:00:00] Dummy-16 : INFO - keep active thread started
```

Usage
------------------------

The important commands are:

* add (label|mention) (.*)
* disable (all|label|mention|review)
* enable (all|label|mention|review)
* list (all|enabled|label|mention|username)
* remove (label|mention) (.*)
* username (.*)

**add** - will add the subscription to the user asking.  It needs the option of what type to
remove followed by the text of the subscription.

**disable** - will disable notifications selectively or for all depending on the selection.

**enable** - will enable notifications selectively or for all depending on the selection.

**list** - will list details about the subscriptions for the user asking.  It needs the option of what to list provided.

**remove** - will remove the subscription from the user asking.  It needs the option of what type to 
add followed by the text of the subscription.

**username** - will set the github user name to link to for certain kind of notifications.

 
State
-------------------------

Currently subscriptions to mentions, labels, review requests, and assigned requests are functional when inspecting pull request
comments when using webhooks.  When using channel scraping only keyword mentions are available. Branches can be subscribed to,
but no effect is taken.

License
-------------------------------

See LICENSE file.  MPL 2.0.

Plan
-------------------------

There are a number of items I'd like to do.

* add enabled disable support for the user
* add some sort of logging
* tests ;_;
* figure out how to make this installable
* hand define the help menu; alter based on admin permission
* enhance channel configurations through admin actions

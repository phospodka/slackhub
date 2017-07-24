Slackhub
========================

Slackhub is a Github integration for slack that aims to provide direct notification for keyword matching and branch
updates.  This is done by messaging the bot commands to manage subscriptions to keywords or full branch names.  

Dependencies
------------------------

Relies heavily on [slacker](https://github.com/os/slacker), [slackbot](https://github.com/lins05/slackbot), and
[flask](https://github.com/pallets/flask) Python projects.

Install the main requirements with:

`pip install -r requirements.txt`

Everything is tested using Python version 3.4

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
[DD/MM/YYYY 00:00:00] Initializing slackbot
[DD/MM/YYYY 00:00:00] Initializing flask
[DD/MM/YYYY 00:00:00] loading plugin "slackhub"
[DD/MM/YYYY 00:00:00] registered respond_to plugin "list_actions" to "list (all|branch|enabled|label|mention|username)"
[DD/MM/YYYY 00:00:00] registered respond_to plugin "add_actions" to "add (branch|label|mention) (.*)"
[DD/MM/YYYY 00:00:00] registered respond_to plugin "remove_actions" to "remove (branch|label|mention) (.*)"
[DD/MM/YYYY 00:00:00] registered respond_to plugin "disable_notifications" to "disable (all|branch|label|mention|review)"
[DD/MM/YYYY 00:00:00] registered respond_to plugin "enable_notifications" to "enable (all|branch|label|mention|review)"
[DD/MM/YYYY 00:00:00] registered respond_to plugin "set_username" to "username (.*)"
[DD/MM/YYYY 00:00:00] connected to slack RTM api
[DD/MM/YYYY 00:00:00] keep active thread started
```

Usage
------------------------

The important commands are:

* add (branch|label|mention) (.*)
* disable (all|branch|label|mention|review)
* enable (all|branch|label|mention|review)
* list (all|branch|enabled|label|mention|username)
* remove (branch|label|mention) (.*)
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
* finish branch subscription functionality
* add any missing support for mentions
* add some sort of logging
* tests ;_;
* figure out how to make this installable

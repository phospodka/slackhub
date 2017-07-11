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

Currently needs my fork of [slackbot](https://github.com/phospodka/slackbot) to handle processing messages from bots.
This is a temporary measure until I get the web hook processing complete.  After downloading run:

`pip install -e {location of download}`

Everything is tested using Python version 3.4

Usage
------------------------

The important commands are:

* list (all|branch|mention)
* remove (branch|mention) (.*)
* add (branch|mention) (.*)


Bad command "help", You can ask me one of the following questions:
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

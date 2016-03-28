Slackhub
========================

Slackhub is a Github integration for slack that aims to provide direct notification for keyword matching and branch
updates.  This is done by messaging the bot commands to manage subscriptions to keywords or full branch names.  

Relies heavily on [slacker](https://github.com/os/slacker) and [slackbot](https://github.com/lins05/slackbot) Python 
projects.

Usage
------------------------

The important commands are:

* list (all|branch|mention)
* remove (branch|mention) (.*)
* add (branch|mention) (.*)

**list** - will list details about the subscriptions for the user asking.  It needs the option of what to list provided.

**remove** - will remove the subscription from the user asking.  It needs the option of what type to 
add followed by the text of the subscription. 
 
**add** - will add the subscription to the user asking.  It needs the option of what type to 
remove followed by the text of the subscription.
 
State
-------------------------

Currently subscriptions to mentions are functional when inspecting pull request comments.  Branches can be subscribed 
to, but no effect is taken.

License
-------------------------------

See LICENSE file.  MPL 2.0.

Plan
-------------------------

There are a number of items I'd like to do.

* add enabled disable support for the user
* finish branch subscription functionality
* add any missing support for mentions
* figure out how to have the bot pm you, not from slackbot; there has to be a way
* add some sort of logging
* tests ;_;

from slackbot.bot import listen_to
from slackhub.dispatcher import post_message
from slackhub.persister import get_cache

"""
Handles channel listening.
"""


@listen_to('.*')
def github_listener(message):
    """
    Super special listener for github message processing.
    :param message: message body that contains all the info
    """
    # listen to all, but then filter on if the message is a bot message? it is part of that message
    # message.body.subtype = 'bot_message'
    # message.body.bot_id = 'the bots id'
    # message.body.type = 'message'
    # then maybe could display exact text?
    #print(message.body.keys())

    # only look at bot_messages; maybe only look at specific bot_id's too
    if message.body['subtype'] == 'bot_message':
        # get the message text so we can process it for subscriptions
        attachments = message.body['attachments']

        for attachment in attachments:
            text = attachment.get('text', '').lower()
            #title = attachments.get('title', '')
            pretext = attachment.get('pretext', '').lower()
            footer = attachment.get('footer', '').lower()
            #print(json.dumps(attachment))

            # process message text against all subscriptions
            for user, details in get_cache().items():
                mentions = details['mention']
                branches = details['branch']
                usertype = details['type']

                # super hacky way to only look at comments
                # missing the review summary message as it does not mark itself
                # may have to abandon this filtering and just always peek in 'text'
                if 'new comment by' in pretext \
                        or 'new comment on' in pretext \
                        or 'pull request submitted by' in pretext \
                        or 'comment by' in footer:
                    for m in mentions:
                        if m.lower() in text:
                            post_message(user, usertype, attachment)
                            break  # only notify once per user

                for b in branches:
                    pass

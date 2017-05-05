import logging
import logging.config
import json
import sys
import threading

from flask import Flask, request
from slackbot import settings
from slackbot.bot import Bot
from slacker import Slacker
from slackhub.webhooker import github_router

# hack for now to include slackhub as a module until I get the egg link working
sys.path.append('..')

# WSGI used for web hooking
app = Flask(__name__)

# direct access to the slack API when needed for special actions
slack = Slacker(settings.API_TOKEN)

logger = logging.getLogger(__name__)


"""
The slackhub bot.  The program to start to get things trucking.  Make sure to add the API_TOKEN from
slack to the local_settings.py.  Persistent data for usage subscriptions will be saved to the ./data
folder.  Be sure to have write permissions.
"""


def main():
    """
    Function that starts if executing the module
    """
    kw = {
        'format': '[%(asctime)s] %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.DEBUG if settings.DEBUG else logging.INFO,
        'stream': sys.stdout,
        }
    logging.basicConfig(**kw)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)
    logger.info(str(sys.path))

    # both slackbot and flask execute til interruption so need to be in their own thread.
    # use daemons so that we can just kill the parent process and not wait for closure.
    slackd = threading.Thread(name='slackd', target=slackbot_init, daemon=True)
    webhookd = threading.Thread(name='webhookd', target=webhook_init, daemon=True)

    # starts the threads
    slackd.start()
    webhookd.start()

    # join the threads to keep the main program running so they can do their work
    slackd.join()
    webhookd.join()


def slackbot_init():
    logger.info('Initializing slackbot')
    bot = Bot()
    bot.run()


def webhook_init():
    logger.info('Initializing flask')
    app.run(host='0.0.0.0')


@app.route("/", methods=['GET', 'POST'])
def webhook_sink():
    # needs to handle trusted listening to known hosts and maybe just POST
    github_router(request.headers.environ['HTTP_X_GITHUB_EVENT'], request.json)
    return "OK"


def get_username(msg):
    """
    Get the username from the message body
    :param msg: message body to parse
    :return: username from the message
    """
    msguser = json.loads(slack.users.info(msg.body['user']).raw)
    return msguser['user']['name']


# main it up a notch
if __name__ == '__main__':
    main()

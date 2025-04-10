import logging
import logging.config
import sys
import threading

from dotenv import load_dotenv
from flask import Flask, abort, request

import slackhub.bolter as bolter
import slackhub.utiler as utiler
import slackhub.webhooker as webhooker # need to fix circular dependency

#from slackhub.webhooker import github_router

"""
The slackhub bot.  The program to start to get things trucking.  Make sure to add the API_TOKEN from
slack to the local_settings.py.  Persistent data for usage subscriptions will be saved to the ./data
folder.  Be sure to have write permissions.
"""

# load the env to get environment variables from the .env file
load_dotenv()

# WSGI used for web hooking
flask = Flask(__name__)

logger = logging.getLogger(__name__)


def main():
    """
    Function that starts if executing the module
    """
    kw = {
        'format': '[%(asctime)s] %(name)s : %(threadName)s : %(levelname)s - %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.DEBUG if utiler.get_bool('DEBUG') else logging.INFO,
        'stream': sys.stdout,
        }
    logging.basicConfig(**kw)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
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
    """
    Thread target for initializing slackbot
    """
    logger.info('Initializing slackbot')
    bolter.start()


def webhook_init():
    """
    Thread target for initializing flask
    """
    logger.info('Initializing flask')
    #context = ('local.crt', 'local.key')#certificate and key files
    #flask.run(debug=True, ssl_context=context)
    flask.run(host='0.0.0.0')


@flask.route("/slackhub/<token>", methods=['GET', 'POST'])
def webhook_sink(token):
    """
    Entry point that needs to be publicly exposed for web hook processing.  The end of the route
    needs to be a token that is defined in settings as SLACKHUB_TOKEN.  This will be used as a
    pseudo secret so we can ignore requests from untrusted sources.
    :param token: SLACKHUB_TOKEN parsed from the end of the request URL
    :return: a http status code dependent on success or failure
    """
    if utiler.get_env('SLACKHUB_TOKEN') != token or not utiler.get_bool('WEBHOOK_ENABLED'):
        abort(403)
    elif request.method == 'GET':
        return 'boop'
    # needs to handle trusted listening to known hosts and maybe just POST
    webhooker.github_router(request.headers.environ['HTTP_X_GITHUB_EVENT'], request.json)
    return "OK"


@flask.route("/oauth", methods=['GET', 'POST'])
def oauth_redirect_url():
    """
    Oauth redirect url
    """
    return "OK"


# main it up a notch
if __name__ == '__main__':
    main()

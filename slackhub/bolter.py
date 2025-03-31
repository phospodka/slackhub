import logging
import re

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import slackhub.adminer as adminer
import slackhub.configurer as configurer
import slackhub.helper as helper
import slackhub.utiler as utiler


"""
The slackhub bot.  The program to start to get things trucking.  Make sure to add the API_TOKEN from
slack to the local_settings.py.  Persistent data for usage subscriptions will be saved to the ./data
folder.  Be sure to have write permissions.
"""

# load the env to get environment variables from the .env file
load_dotenv()

app = App(token=utiler.get_env('SLACK_BOT_TOKEN'))

logger = logging.getLogger(__name__)

def start():
    SocketModeHandler(app, utiler.get_env('SLACK_APP_TOKEN')).start()

@app.message(re.compile('help', re.IGNORECASE))
def help_message_handler(message, say):
    # say() sends a message to the channel where the event was triggered
    logger.info('got message')
    response = helper.help_me(message)
    say(response)


@app.event("message")
def direct_message_handler(body, say):
    # say() sends a message to the channel where the event was triggered
    logger.info('got event message')
    event = body.get('event')
    say(command_parser(event))
    #say(f"Thanks for messaging me, <@{event['user']}>!")


@app.event("app_mention")
def bot_mention_handler(body, say):
    # say() sends a message to the channel where the event was triggered
    logger.info('got event mention')
    event = body.get('event')
    say(command_parser(event))
    #say(f"Thanks for mentioning me, <@{event['user']}>!")


adminer_actions = [
    adminer.list_channel_actions,
    adminer.add_admin, adminer.remove_admin, adminer.list_admin,
    adminer.add_channel_actions, adminer.add_channel_repo_actions, adminer.add_channel_repos,
    adminer.remove_channel_actions, adminer.remove_channel_repo_actions, adminer.remove_channel_repos,
    adminer.disable_notifications, adminer.disable_repo_notifications,
    adminer.enable_notifications, adminer.enable_repo_notifications]

configurer_actions = [
    configurer.list_actions,
    configurer.add_actions, configurer.add_repo_actions, configurer.add_repos,
    configurer.remove_actions, configurer.remove_repo_actions, configurer.remove_repos,
    configurer.disable_notifications, configurer.disable_repo_notifications,
    configurer.enable_notifications, configurer.enable_repo_notifications,
    configurer.set_username]


def command_parser(message):
    for fun in configurer_actions:
        try:
            return fun(message)
        except Exception as e:
            print(f'Exception: {e}')
            pass
    return utiler.get_env('DEFAULT_REPLY')

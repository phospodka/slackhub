import logging
import logging.config
import sys

from slackbot import settings
from slackbot.bot import Bot

logger = logging.getLogger(__name__)

"""
The slackhub bot.  The program to start to get things trucking.  Make sure to add the API_TOKEN from slack to the
local_settings.py.  Persistent data for usage subscriptions will be saved to the ./data folder.  Be sure to have
write permissions.
"""


def main():
    kw = {
        'format': '[%(asctime)s] %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.DEBUG if settings.DEBUG else logging.INFO,
        'stream': sys.stdout,
        }
    logging.basicConfig(**kw)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)
    bot = Bot()
    bot.run()


# main it up a notch
if __name__ == '__main__':
    main()

# Twitter To Telegram
# Telegram Libs
from telegram.ext import Updater

# Python Libs
import time
import schedule

# Other Functions
from telegram_funtions import send_to_telegram
from airtable_funtions import get_delay, get_account_info
from twitter_functions import create_tweepy_object, scrape_twitter

# Configs
from config import BOT_TOKEN

# Setup logging
import logging
logging.basicConfig(format='%(asctime)s  %(levelname)s:%(message)s', filename='twitter.log', filemode='a', level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to get New Tweets
def run_process(record_id):
    try:
        airtable, info_field = get_account_info(record_id)
        chat_id, tweet_text, media_array, silent_notification = scrape_twitter(airtable, twapi, info_field)
        send_to_telegram(updater, chat_id, tweet_text, media_array, silent_notification)
    except Exception as e: logger.error("run_process - {}".format(e))

# Initialize Twitter API
twapi = create_tweepy_object()
# Setup the updater
updater = Updater(BOT_TOKEN, use_context=True)

# Main
if __name__ == "__main__":
    # Get Delay
    delay_array = get_delay()

    # CREATE SHCEDULED TASKS
    for entry in delay_array:
        try:
            delay = int(entry[1])
        except:
            delay = 360
        record_id = str(entry[0])
        schedule.every(delay).seconds.do(run_process, record_id)

    # Run the Schedule
    while 1:
        schedule.run_pending()
        time.sleep(10)

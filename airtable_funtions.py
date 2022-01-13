# Airtable
from pyairtable import Table

# Configs
from config import DB_AIRTABLE_ID, TABLE_NAMES, API_KEY

# Setup logging
import logging
logger = logging.getLogger(__name__)

# Get from the airtable the delay
def get_delay():
    try:
        airtable = Table(API_KEY, DB_AIRTABLE_ID, TABLE_NAMES[0])
        info_field = airtable.all()

        info_field_array = []
        for c_a in info_field:
            single_entry_array = []
            single_entry_array.append(c_a.get('id'))
            single_entry_array.append(c_a.get('fields').get('Delay'))
            info_field_array.append(single_entry_array)

        return info_field_array
    except Exception as e:
        logging.error("get_delay - {}".format(e))

# Update the Tweet ID inside the airtable if there is a new tweet
def update_posted_field(airtable, record_id_tweet_id):
    try:
        record_id = record_id_tweet_id[0]
        new_tweet_id = str(record_id_tweet_id[1])
        airtable.update(record_id, {'Tweet-ID': new_tweet_id})
    except Exception as e: logger.error("update_posted_field - {}".format(e))

# Get from the airtable: Twitter, Telegram, latest tweet id.
def get_account_info(record_id):
    try:
        airtable = Table(API_KEY, DB_AIRTABLE_ID, TABLE_NAMES[0])
        info_field = airtable.get(record_id)

        single_entry_array = []
        single_entry_array.append(info_field.get('id'))
        single_entry_array.append(info_field.get('fields').get('Twitter'))
        single_entry_array.append(info_field.get('fields').get('Telegram'))
        single_entry_array.append(info_field.get('fields').get('Tweet-ID'))
        single_entry_array.append(info_field.get('fields').get('RT'))
        single_entry_array.append(info_field.get('fields').get('Silent'))

        return airtable, single_entry_array
    except Exception as e: logger.error("get_account_info - {}".format(e))

# Clean some checkboxes
def clean_check_boxes(silent_notification, retweets, latest_post):
    # Clean silent notification
    if(not silent_notification):
        silent_notification = False
    # Clean Retweets
    if(not retweets):
        retweets = False
    # Clean latest_post
    if(not latest_post):
        latest_post = False
    return silent_notification, retweets, latest_post

# Python Libs
import html
import re

# Twitter Lib
import tweepy

# Other Functions
from airtable_funtions import clean_check_boxes, update_posted_field

# Configs
from config import (TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, 
                        TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

# Setup logging
import logging
logger = logging.getLogger(__name__)

# Create Tweepy Object
def create_tweepy_object():
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    try:
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    except KeyError:
        logger.info("Either TWITTER_ACCESS_TOKEN or TWITTER_ACCESS_TOKEN_SECRET "
                "Tweepy will be initialized in 'app-only' mode")
    twapi = tweepy.API(auth)
    logger.info("Setup the Twitter API Object")

    return twapi

# Get the latest tweet from twitter
def fetch_tweet(twitter_account_name, twapi, latest_post, Retweets):
    try:
        # If First Run
        if not latest_post:
            tweets = twapi.user_timeline(screen_name=twitter_account_name,
                                    count=1, tweet_mode='extended',
                                    include_rts=Retweets)
        else:
            tweets = twapi.user_timeline(screen_name=twitter_account_name,
                                    since_id=latest_post, tweet_mode='extended',
                                    include_rts=Retweets)
    except Exception as e: logger.error("fetchTweet - {}".format(e))

    try:
        # No New Tweets
        if(not tweets):
            return None, None, None
        else:
            logger.info("Found New Tweets")
            tweet_not_sent = tweets[-1]
            # If tweet contains media, get it back
            photo_urls = get_photo(tweet_not_sent)
            video_urls = get_video(tweet_not_sent)
            media_array = format_media(photo_urls, video_urls)
            # Clean the tweet Text
            tweet_text = clean_tweet_text(tweet_not_sent)
            # Full RT
            if Retweets:
                tweet_text = get_full_retweet_text(tweet_text, tweet_not_sent)
            # Clean Picture URL and Send
            tweet_text = cleaning_pic_URL(tweet_text)
            return tweet_not_sent.id, tweet_text, media_array
    except Exception as e:
        logger.error("fetchTweet - {}".format(e))
        return None, None, None

# Send twitter message to telegram
def scrape_twitter(airtable, twapi, info_field):
    try:
        record_id = info_field[0].strip()
        twitter_account_name = info_field[1].strip()
        telegram_chat_id = info_field[2].strip()
        latest_post = info_field[3]
        retweets = info_field[4]
        silent_notification = info_field[5]
    except Exception as e: logger.error("scrapeTwitter - {}".format(e))

    # Clean the checkBoxes
    silent_notification, retweets, latest_post = clean_check_boxes(silent_notification, retweets,
                                                                    latest_post)

    try:
        # Get Tweets
        tweet_id, tweet_text, media_array = fetch_tweet(twitter_account_name, twapi, latest_post, retweets)
        # No New Tweets
        if tweet_id is None:
            return telegram_chat_id, None, None, None
        # New Tweets But will not send
        elif (tweet_text is None):
            update_posted_field(airtable, [record_id, tweet_id])
            return telegram_chat_id, None, None, None
        # Send
        else:
            update_posted_field(airtable, [record_id, tweet_id])
            return telegram_chat_id, tweet_text, media_array, silent_notification
    except Exception as e:
        logger.error("scrapeTwitter - {}".format(e))
        return telegram_chat_id, None, None, None

# Get Photo(s) from Tweet
def get_photo(tweet):
    extensions = ('.jpg', '.jpeg', '.png', '.gif')
    pattern = '[(%s)]$' % ')('.join(extensions)
    photo_urls = []
    count = 0

    if 'media' in tweet.entities:
        for media in tweet.extended_entities['media']:
            try:
                photo_urls.append(media['media_url_https'])
                count = count + 1
            except:
                pass
    else:
        for url_entity in tweet.entities['urls']:
            expanded_url = url_entity['expanded_url']
            if re.search(pattern, expanded_url):
                photo_urls.append(expanded_url)
                break
    if photo_urls:
        for photo_url in photo_urls:
            logger.info("Found media URL in tweet: " + photo_url)
    return photo_urls

# Get Video from Tweet
def get_video(tweet):
    video_urls = []
    if 'media' in tweet.entities:
        for media in tweet.extended_entities['media']:
            if 'video_info' in media:
                video = media['video_info']
                video = video['variants'][-1]
                video_urls.append(video['url'])
    return video_urls

# Format media Array
def format_media(photo_urls, video_urls):
    if len(video_urls) >= 1:
        return ['Video', video_urls]
    elif len(photo_urls) >= 1:
        if len(photo_urls) >= 2:
            return ['Photos', photo_urls]
        else:
            return ['Photo', photo_urls]
    else:
        return None

# Clean picture URL from text
def cleaning_pic_URL(text):
    text = re.sub(r'https://t.co/[\w]*',"", text)
    return text

# Escape twitter username mentions
def markdown_twitter_usernames(text):
    return re.sub(r'@([A-Za-z0-9_\\]+)',
                  lambda s: '@ {username}'
                  .format(username=s.group(1).replace(r'\_', '_')),
                  text)

# Clean the tweet Text
def clean_tweet_text(tweet):
    try:
        tweet_text = html.unescape(tweet.full_text)
        for url_entity in tweet.entities['urls']:
            expanded_url = url_entity['expanded_url']
            indices = url_entity['indices']
            display_url = tweet.full_text[indices[0]:indices[1]]
            tweet_text = tweet_text.replace(display_url, expanded_url)
        tweet_text = str(tweet_text)
        tweet_text = markdown_twitter_usernames(tweet_text)
        return tweet_text
    except Exception as e: logger.error(e)

# Get the full Retweet Text
def get_full_retweet_text(tweet_text, tweet):
    try:
        if tweet_text.startswith("RT @") == True or tweet_text.startswith("rt @") == True:
            rtUsername = tweet_text.split(':')[0]
            tweet_text = rtUsername + ": " + tweet.retweeted_status.full_text
            tweet_text = str(tweet_text)
            tweet_text = markdown_twitter_usernames(tweet_text)
        return tweet_text
    except Exception as e: logger.error(e)

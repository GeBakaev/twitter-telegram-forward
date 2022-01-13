# Telegram Libs
from telegram import ParseMode
from telegram import InputMediaPhoto

# Setup logging
import logging
logger = logging.getLogger(__name__)

# Send the message to telegram
def send_message(context, chat_id, tweet_text, silent_notification):
    # Send the data to the specified telegram groups/channels
    try:
        if tweet_text is None:
            pass
            # logging.info("All upto date on {}".format(str(chat_id)))
        else:
            context.bot.sendMessage(
                chat_id=chat_id,
                disable_web_page_preview=False,
                disable_notification= silent_notification,
                text=tweet_text,
                parse_mode=ParseMode.HTML)
            logging.info("Sent new tweets to {}".format(chat_id))
    except Exception as e: logging.error("sendMessage - {}".format(e))

# Send Video To telegram
def send_single_video(context, chat_id, tweet_text, media_array, silent_notification):
    try:
        video_url = media_array[0]
        context.bot.sendVideo(
            chat_id=chat_id,
            disable_notification=silent_notification, 
            video=video_url,
            caption=tweet_text,
            parse_mode=ParseMode.HTML,
            supports_streaming=True)
        logging.info("Sent new tweets to {}".format(chat_id))
    except Exception as e: logging.error("sendSingleVideo - {}".format(e))

# Send single Photo To telegram
def send_single_photo(context, chat_id, tweet_text, media_array, silent_notification):
    try:
        photo_url = media_array[0]
        context.bot.sendPhoto(
            chat_id=chat_id,
            disable_notification=silent_notification,
            photo=photo_url,
            caption=tweet_text,
            parse_mode=ParseMode.HTML)
        logging.info("Sent new tweets to {}".format(chat_id))
    except Exception as e: logging.error("sendSinglePhoto - {}".format(e))

# Prepare to send multiple Photos to telegram
def prepare_multiple_photos(photo_url, tweet_text):
    mediaList = []
    count = 0
    for photo in photo_url:
        if count == 0:
            photoOBject = InputMediaPhoto(media=photo, caption=tweet_text, parse_mode=ParseMode.HTML)
        else:
            photoOBject = InputMediaPhoto(media=photo)
        mediaList.append(photoOBject)
        count = count + 1
    return mediaList

# Send multiple Photos to telegram
def send_multiple_photos(context, chat_id, photo_url, silent_notification):
    try:
        context.bot.sendMediaGroup(
            chat_id=chat_id,
            disable_notification=silent_notification,
            media=photo_url)
        logging.info("Sent new tweets to {}".format(chat_id))
    except Exception as e: logging.error("sendMultiplePhotos - {}".format(e))

# Determine to send Photo, Photo(s), Video or Text only
def send_to_telegram(context, chat_id, tweet_text, media_array, silent_notification):
    # If tweet contains media
    if media_array:
        if media_array[0] == "Video":
            send_single_video(context, chat_id, tweet_text, media_array[1], silent_notification)
        elif media_array[0] == "Photo":
            send_single_photo(context, chat_id, tweet_text, media_array[1], silent_notification)
        elif media_array[0] == "Photos":
            photo_url = prepare_multiple_photos(media_array[1], tweet_text)
            send_multiple_photos(context, chat_id, photo_url, silent_notification)
    # Tweet contains text only
    else:
        send_message(context, chat_id, tweet_text, silent_notification)

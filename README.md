# Twitter Telegram Forward

A Bot that Forwards Tweets to Telegram using Airtable as a Database.

### Features:

* Handles multiple twitter and telegram channels.
* Custom delay for each entry.
* Automatically embeds images and videos to telegram.
* ReTweets can be enabled or disabled.
* Sends telegram messages with silent notifications.

## Setup
### Airtable Database
1. Create an ([Airtable Account](https://airtable.com/)
2. Create a new Workspace. 
3. Add a new base and import the "Twitter Telegram.csv" file. Or create from scratch using the template below:
    ```
        id(Single Line Text),Twitter(Single Line Text),Telegram(Single Line Text),Tweet-ID(Single Line Text),
        RT(Checkbox),Silent(Checkbox),Delay(Number)
    ```
4. Get the Airtable ID:
    * pressing the "?" icon near "HELP" (Top Right). 
    * Clicking on "API Documentation".
    * Copy the ID in the middle of the page after the words "The ID of this base is ".
    * Add the ID to the DB_AIRTABLE_ID in the config file. Note: Omit the do at the end.
5. Get your Airtable API Key:
    * Go to https://airtable.com/account
    * Your API Key should be under "API"
    * Add the API Key to the API_KEY in the config file.

### Telegram Bot
1. You can create a new bot via ([@BotFather](https://telegram.me/BotFather)).
2. Add the Bot token you got to the BOT_TOKEN in the config file.

### Twitter API
1. You will need an Application-only authentication token from Twitter ([more info here](https://dev.twitter.com/oauth/application-only)). Optionally, you can provide a user access token and secret.
You can get this by creating a Twitter App [here](https://apps.twitter.com/).

Bear in mind that if you don't have added a mobile phone to your Twitter account you'll get this:

>You must add your mobile phone to your Twitter profile before creating an application. Please read https://support.twitter.com/articles/110250-adding-your-mobile-number-to-your-account-via-web for more information.

2. Get a consumer key, consumer secret, access token and access token secret (the latter two are optional), fill in your `config.py`.

### Running the Bot
4. `pip install -r requirements.txt`
5. Run it! `python main.py` (Check the Filling the Airtable Base section before.)


## Filling the Airtable Base

* Both Twitter and Telegram fields should start with @.
* Private channels or normal user chats can also be used. You can get the ID using [@JsonDumpBot](https://t.me/JsonDumpBot).
    * No need to start with a @ in this case.
* The Tweet-ID field can be left empty. On the first run, the bot will fill it with the latest tweet ID.
* RT Field need to be checked in order to forward Retweets.
* Delay field is in seconds. If left empty, it will be set to 360 seconds.
* After adding a new row in the airtable, the bot needs to be restarted. If a row is changed, the bot does NOT need to be restarted.

## TODO

* Create Heroku Auto Setup.
* Setup Cron in order to keep bot running
* Create Logic for Replies (Only forward user threads).
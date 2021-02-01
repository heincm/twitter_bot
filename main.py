import json
import requests
import tweepy as tp
import constants
import datetime

consumer_key = constants.consumer_key
consumer_secret = constants.consumer_secret
access_token = constants.access_token
access_secret = constants.access_secret

auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tp.API(auth)

user = api.me()


def follow_followers():
    follower = api.followers(user.screen_name)[0]
    try:
        follow_back(follower)
    except:
        print("No more followers to follow")


def follow_back(follower):
    if follower.following:
        return
    else:
        api.create_friendship(follower.id)
        api.update_status("Hello there, @" + follower.screen_name + ' 👋! Thanks for following! 🤖')


def look_for_mentions():
    for mention in api.mentions_timeline():
        try:
            if mention.author.following:
                return
            else:
                api.create_friendship(mention.author.id)
        except:
            print('something went wrong')


def call_api():
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json').json()
    response = str(response)
    response = response.replace("\'", "\"")
    middle_man = json.loads(response)
    usd_amt = middle_man["bpi"]["USD"]["rate"]
    usd_amt = usd_amt[:-2]
    gbp_amt = middle_man["bpi"]["GBP"]["rate"]
    gbp_amt = gbp_amt[:-2]
    eur_amt = middle_man["bpi"]["EUR"]["rate"]
    eur_amt = eur_amt[:-2]
    bitcoin_price = "Current Bitcoin Price:\nUSD $" + usd_amt + '\nGBP £' + gbp_amt + '\nEuro €' + eur_amt + '\n#bitcoin #btc $btc #btcusd #btcgbp #btceur #crypto #cryptocurrency'
    return bitcoin_price


def search_relevant_tweets():
    tag = ("bitcoin", "btc", "crypto", "cryptocurrency", "#bitcoin", "#btc", "$btc")
    for tweet in tp.Cursor(api.search, tag, result_type="recent", lang="en").items(21):
        try:
            favorite_a_tweet(tweet)
            print("tweet favorited")
        except tp.TweepError as e:
            print(e.reason)


def favorite_a_tweet(tweet):
    #  have to get the use the api method to get the id to see actual
    #  info. on whether tweet has been favorited or not
    new_tweet = api.get_status(tweet.id)
    if (new_tweet.favorited is False) and (tweet.user.id != user.id):
        return tweet.favorite()
    return


def check_time():
    now = datetime.datetime.now()
    two_after_the_hour = now.replace(minute=52)
    sometime_after_the_hour = now.replace(minute=57)

    if two_after_the_hour < now < sometime_after_the_hour:
        return search_relevant_tweets()
    print("out of range")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    follow_followers()
    api.update_status(call_api())
    look_for_mentions()
    check_time()

import os
import json
import requests
import tweepy as tp
import constants
from time import sleep

consumer_key = constants.consumer_key
consumer_secret = constants.consumer_secret
access_token = constants.access_token
access_secret = constants.access_secret

auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tp.API(auth)

user = api.me()
print(user.name)
print(user.location)


def follow_followers():
    for follower in api.followers(user.screen_name):
        try:
            # follower.follow()
            print('follower ' + follower.screen_name)
            # api.create_friendship(follower.screen_name)
            print('following ' + follower)
        except:
            print("No more followers to follow")


def call_api():
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json').json()
    print(response)
    response = str(response)
    response = response.replace("\'", "\"")
    middle_man = json.loads(response)
    print('disclaimer ' + middle_man["disclaimer"])
    usd_amt = middle_man["bpi"]["USD"]["rate"]
    usd_amt = usd_amt[:-2]
    print('USD Amount $' + usd_amt)
    bitcoin_price = 'Current Bitcoin Price: USD $' + usd_amt
    return bitcoin_price


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    follow_followers()
    api.update_status(call_api())

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



def follow_followers():
    for follower in api.followers(user.screen_name):
        try:
            follow_back(follower)
        except:
            print("No more followers to follow")


def follow_back(follower):
    if follower.following:
        return
    api.create_friendship(follower.id)


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
    bitcoin_price = 'Current Bitcoin Price:\nUSD $' + usd_amt + '\nGBP £' + gbp_amt + '\nEuro €' + eur_amt + '\n#bitcoin #btc $btc #btcusd #btcgbp #btceur #crypto #cryptocurrency'
    return bitcoin_price


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    follow_followers()
    api.update_status(call_api())

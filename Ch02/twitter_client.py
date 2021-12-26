# Chap02-03/twitter_client.py
# connection to Twitter client

import os
import sys
# requires install of python-decouple
from decouple import config

from tweepy import API
from tweepy import OAuthHandler

def get_twitter_auth():
    """Setup Twitter authentication.
    Return: tweepy.OAuthHandler object
    """

    try:
        consumer_key = config('TWITTER_CONSUMER_KEY')
        consumer_secret = config('TWITTER_CONSUMER_SECRET')
        access_token = config('TWITTER_ACCESS_TOKEN')
        access_secret = config('TWITTER_ACCESS_SECRET')
    except KeyError:
        sys.stderr.write("TWITTER_* environment variables not set\n")
        sys.exit(1)

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth

def get_twitter_client():
    """Setup Twitter API client.
    Return: tweepy.API object
    """
    auth = get_twitter_auth()
    client = API(auth)
    return client

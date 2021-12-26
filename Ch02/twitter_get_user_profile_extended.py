# twitter_get_user_profile_extended.py
# get the profile of a user and also those of followers and friends
# modified for latest version of tweepy
# last revised 27Nov2021

# note: followers are those friending the user

import os
import sys
import json
import time
import math
from tweepy import Cursor
from twitter_client import get_twitter_client

MAX_FRIENDS = 15000

def usage():
    print("Usage:")
    print("python {} <username>".format(sys.argv[0]))

def paginate(items, n):
    """Generate n-sized chunks from items

    :param items: list of items to paginate
    :param n: size of chunks
    :return: individual chunks (as a list of lists)

    """
    for i in range(0, len(items), n):
        yield items[i:i+n]

if __name__ == '__main__':
    # validation for command line execution
    #if len(sys.argv) != 2:
    #    usage()
    #    sys.exit(1)

    # for terminal execution
    try:
        screen_name = sys.argv[1]
    except Exception as e:
        pass

    # hardwired
    #screen_name = "sberman8"
    client = get_twitter_client()
    dirname = "users/{}".format(screen_name)

    # set max page count
    max_pages = math.ceil(MAX_FRIENDS / 5000)
    try:
        os.makedirs(dirname, mode=0o755, exist_ok=True)
    except OSError:
        print("Directory {} already exists".format(dirname))
    except Exception as e:
        print("Error while creating directory {}".format(dirname))
        print(e)
        sys.exit(1)

    # get followers for a given user
    print("Getting followers")
    fname = f"{dirname}/followers.jsonl"
    with open(fname, 'w') as f:
        for followers in Cursor(client.get_follower_ids, screen_name=screen_name).pages(max_pages):
            for chunk in paginate(followers, 100):
                users = client.lookup_users(user_id=chunk)
                for user in users:
                    f.write(json.dumps(user._json)+"\n")

            if len(followers) == 5000:
                print("More results available. Sleeping for 60 seconds to avoid rate limit")
                time.sleep(60)

    # get friends for a given user
    print("Getting friends")
    fname = f"{dirname}/friends.jsonl"
    with open(fname, 'w') as f:
        for friends in Cursor(client.get_friend_ids, screen_name=screen_name).pages(max_pages):
            for chunk in paginate(friends, 100):
                users = client.lookup_users(user_id=chunk)
                for user in users:
                    f.write(json.dumps(user._json)+"\n")
            if len(friends) == 5000:
                print("More results available. Sleeping for 60 seconds to avoid rate limit")
                time.sleep(60)

    # get user's profile
    print("Getting user")
    fname = f"{dirname}/user_profile.json"
    with open(fname, 'w') as f:
        profile = client.get_user(screen_name=screen_name)
        f.write(json.dumps(profile._json, indent=4))

# usage:
#    python twitter_get_user_profile_extended.py <username>
# (where param is the root user)

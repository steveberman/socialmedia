# Chap02-03/twitter_get_user_timeline.py
# predecessors: none
# output: user_time_<username>.jsonl

import sys
import json

from tweepy import Cursor
from twitter_client import get_twitter_client

if __name__ == '__main__':
    user = sys.argv[1]
    client = get_twitter_client()
    fname = "user_timeline_{}.jsonl".format(user)
    with open(fname, 'w') as f:
        for page in Cursor(client.user_timeline, screen_name=user,
                           count=200).pages(16):
            for status in page:
                # _json is tweepy method with full contents as json string
                f.write(json.dumps(status._json)+"\n")
                # this is for readability but reads in subsequent files cannot use this
                #f.write(json.dumps(status._json, indent=3)+"\n")

# usage:
#   python twitter_get_user_timeline.py sberman8
# keys:
#   text: contains tweet message
#   user: writer of tweet (id, name, screen name, etc.) - use author method
#   entities: dictionaries of URLs and hashtags

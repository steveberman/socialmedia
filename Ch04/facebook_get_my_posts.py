# Chap04/facebook_get_my_posts.py
# get posts for author
# predecessors: none
# outputs: to my_posts.jsonl - list of tweets as dictionaries, time and message

import os
import json
import facebook
import requests
from decouple import config

if __name__ == '__main__':
    token = config('FACEBOOK_USER_ACCESS_TOKEN')
    graph = facebook.GraphAPI(token)
    # get_connections takes list of attributes to query from facebook
    posts = graph.get_connections('me', 'posts')
    while True: # keep paginating
        try:
            with open('my_posts.jsonl', 'a') as f:
                for post in posts['data']:
                    # write post text
                    f.write(json.dumps(post)+"\n")

                # get next page
                # NOTE: pagination is not in facebook-sdk, so need to use requests lib directly
                # paging section provides exact URL to query next, including access token, etc.
                posts = requests.get(posts['paging']['next']).json()
        except KeyError:
            # no more pages, break the loop
            break

# usage: python facebook_get_my_posts.py

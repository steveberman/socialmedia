# Chap04/facebook_get_my_posts_extended.py
# get author posts, with more fields than facebook_get_my_posts.py
# NOTE: structure of a post on page 139 of social media text
# NOTE: Post object has more attributes than this

import os
import json
import facebook
import requests
from decouple import config

if __name__ == '__main__':
    token = config('FACEBOOK_USER_ACCESS_TOKEN')
    graph = facebook.GraphAPI(token)
    all_fields = [
        'message',
        'created_time',
        'description',
        'caption',
        'link',
        'place',
        'status_type'
    ]
    # list to string
    all_fields = ','.join(all_fields)

    try:
        os.remove("my_posts.jsonl")
    except:
        pass

    # fields param specifies what to pull
    posts = graph.get_connections('me', 'posts', fields=all_fields)

    while True: # keep paginating until errors out at end
        try:
            with open('my_posts.jsonl', 'a') as f:
                for post in posts['data']:
                    f.write(json.dumps(post)+"\n")

            # get next page
            posts = requests.get(posts['paging']['next']).json()
        except KeyError:
            # no more pages, break the loop
            break

# usage: python facebook_get_my_posts_extended.py
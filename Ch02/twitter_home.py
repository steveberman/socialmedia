# twitter_home.py
# show most recent items on twitter home feed

import json
from tweepy import Cursor
from twitter_client import get_twitter_client

if __name__ == '__main__':
    client = get_twitter_client()
    # Cursor is an iterable, returns Status (tweet) objects
    for idx, status in enumerate(Cursor(client.home_timeline).items(10)):
        # Process a single status
        print(f"*** {idx} ***")
        print(status.text)

    # save to a jsonl file, where each line is a json document
    with open('home_timeline.jsonl', 'w') as f:
        # count is number of items in a page
        # max of 800 items queryable from home timeline
        for page in Cursor(client.home_timeline, count=200).pages(4):
            for status in page:
                f.write(json.dumps(status._json)+"\n")

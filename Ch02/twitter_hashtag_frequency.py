# Chap02-03/twitter_hashtag_frequency.py

import sys
from collections import Counter
import json

def get_hashtags(tweet):
    """ get all hashtags for a tween

    :param tweet: dictionary of Status (tweet) object
    :return: all hashtags, converted to lowercase
    :rtype: list
    """
    entities = tweet.get('entities', {})
    hashtags = entities.get('hashtags', [])
    return [tag['text'].lower() for tag in hashtags]

if __name__ == '__main__':
    fname = sys.argv[1]
    print(fname)
    # load a jsonl file containing some number of tweet json items
    with open(fname, 'r') as f:
        hashtags = Counter()
        for line in f:
            #print(line)
            tweet = json.loads(line)
            # get all hashtags
            hashtags_in_tweet = get_hashtags(tweet)
            # increment hashtag count using the Counter instance
            hashtags.update(hashtags_in_tweet)
            # most_common performs an ordering
            # if fewer than 20, then seems to duplicate
            for tag, count in hashtags.most_common(20):
                print("{}: {}".format(tag, count))

# usage:
#   python twitter_hashtag_frequency.py user_timeline_PacktPub.jsonl
#     where the file is created from a twitter_get_user_timeline.py run

# Chap02-03/twitter_streaming.py
# extend default StreamListening class from tweepy

import sys
import string
import time

# in tweepy 4.0, StreamListener combined into Stream
from tweepy import Stream

# authorization for twitter account - custom
from twitter_client import get_twitter_auth

#region "class_custom_listener"

class CustomListener(Stream):
    """Custom StreamListener for streaming Twitter data."""
    def __init__(self, fname):
        safe_fname = format_filename(fname)
        self.outfile = "stream_%s.jsonl" % safe_fname

    # two methods overridden:
    # both methods reutrn True to continue execution and False to stop
    #   (so return False only on fatal errors)

    def on_data(self, data):
        # callback when data received
        try:
            # store data in a .jsonl file
            with open(self.outfile, 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            sys.stderr.write("Error on_data: {}\n".format(e))
            # short sleep for any network issues
            time.sleep(5)
            return True

    def on_error(self, status):
        # callback for errors from Twitter
        # (codes at https://dev.twitter.com/overview/api/response-codes)
        if status == 420:
            # too many requests!
            sys.stderr.write("Rate limit exceeded\n")
            return False
        else:
            # otherwise, just log the error - redirect stderr if necessary
            sys.stderr.write("Error {}\n".format(status))
            return True

#endregion

def format_filename(fname):
    """Convert fname into a safe string for a file name.
        Return: string
    """
    return ''.join(convert_valid(one_char) for one_char in fname)

def convert_valid(one_char):
    """Convert a character into '_' if "invalid".
        Return: string
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'

if __name__ == '__main__':
    query = sys.argv[1:]           # list of command line interface arguments
    query_fname = ' '.join(query)  # string

    auth = get_twitter_auth()
    twitter_stream = Stream(auth, CustomListener(query_fname))
    twitter_stream.filter(track=query)

# usage:
#   python twitter_streaming.py \#NFL \#NewYorkJets Jets
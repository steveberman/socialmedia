# Chap02-03/twitter_term_frequency.py
# most common terms
#   includes punctuations, so hashtags and usernames are counted separately, as well
#     as various things like quote marks (because using the TweetTokenizer)

import sys
import string
import json
from collections import Counter
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')

def normalize_contractions(tokens):
    """ convert contractions into longer form

    :param tokens: list of tokens to test and change
    :return: revised list of tokens
    :rtype: list
    """
    token_map = {
        "i'm": "i am",
        "you're": "you are",
        "it's": "it is",
        "we're": "we are",
        "we'll": "we will",
    }

    for tok in tokens:
        if tok in token_map.keys():
            for item in token_map[tok].split():
                yield item
        else:
            yield tok

def process(text, tokenizer=TweetTokenizer(), stopwords=[]):
    """Process the text of a tweet:
    - Lowercase
    - Tokenize
    - Stopword removal
    - Digits removal
    Return: list of strings
    """
    text = text.lower()
    tokens = tokenizer.tokenize(text)
    return [tok for tok in tokens if tok not in stopwords and not tok.isdigit()]

if __name__ == '__main__':
    fname = sys.argv[1]
    tweet_tokenizer = TweetTokenizer()
    punct = list(string.punctuation)
    stopword_list = stopwords.words('english') + punct + ['rt', 'via', '...']
    tf = Counter()
    with open(fname, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            # tokenizes, but does not do anything with them
            tokens = process(text=tweet['text'], tokenizer=tweet_tokenizer,
                             stopwords=stopword_list)
            tf.update(tokens)

for tag, count in tf.most_common(20):
    print("{}: {}".format(tag, count))

# interactive only
# frequency graph - show frequencies for top terms - does not label the terms
y = [count for tag, count in tf.most_common(30)]
x = range(1, len(y)+1)
plt.bar(x, y)
plt.title("Term Frequencies")
plt.ylabel("Frequency")
plt.savefig('term_distribution.png')

# usage:
#   python twitter_term_frequency.py user_timeline_johnlucker.jsonl
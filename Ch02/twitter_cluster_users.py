# Chap02-03/twitter_cluster_users.py
# use k-means clustering to segregate users
# predecessors:
#   followers.jsonl file from twitter_get_user_profile_extended.py

import sys
import json

from argparse import ArgumentParser
from collections import defaultdict, OrderedDict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def get_parser():
    # ArgumentParser parses from the command line
    parser = ArgumentParser("Clustering of followers")
    parser.add_argument('--filename')
    # number of clusters
    parser.add_argument('--k', type=int)
    # min and max document frequency
    parser.add_argument('--min-df', type=int, default=2)
    parser.add_argument('--max-df', type=float, default=0.8)
    # max number of features
    parser.add_argument('--max-features', type=int, default=None)
    # if True, then turn off IDF
    parser.add_argument('--no-idf', dest='use_idf', default=True, action='store_false')
    # min and max ngram length
    parser.add_argument('--min-ngram', type=int, default=1)
    parser.add_argument('--max-ngram', type=int, default=1)

    # number of descriptions to print for each cluster
    parser.add_argument('--descriptions', type=int, default=5)
    return parser

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    if args.min_ngram > args.max_ngram:
        print("Error: incorrect value for --min-ngram ({}): it can't be higher than --max-value ({})".format(args.min_ngram,args.max_ngram))
        sys.exit(1)

    with open(args.filename) as f:
        # load data
        users = []
        for line in f:
            profile = json.loads(line)
            users.append(profile['description'])

    # create vectorizer
    vectorizer = TfidfVectorizer(max_df=args.max_df, min_df=args.min_df,
                                 max_features=args.max_features,
                                 stop_words='english',
                                 ngram_range=(args.min_ngram,
                                              args.max_ngram),
                                 use_idf=args.use_idf)
    # fit data
    X = vectorizer.fit_transform(users)

    print("Data dimensions: {}".format(X.shape))

    # perform clustering
    km = KMeans(n_clusters=args.k)
    km.fit(X)
    clusters = defaultdict(list)
    for i, label in enumerate(km.labels_):
        clusters[label].append(users[i])

    # order by cluster number
    clusters = OrderedDict(sorted(clusters.items()))

    # print limited user descriptions for this cluster
    for label, descriptions in clusters.items():
        print('---------- Cluster {}'.format(label+1))
        # number of items added 02Dec2021
        print("  Number of followers = {}".format(len(descriptions)))
        for desc in descriptions[: args.descriptions]:
            print(desc)

# usage:
# python twitter_cluster_users.py \
#   --filename users/marcobonzanini/followers.jsonl \
#   --k 5 \
#   --max-features 200 \
#   --max-ngram 3
#   --descriptions 5

# ex: python twitter_cluster_users.py --filename users/johnlucker/followers.jsonl --k 10 \
#   --max-features 50

# filename and k are only mandatory arguments
# min doc frequency represents number of documents required for term to be kept
# max doc frequency represents percent of documents term can be in

# rule of thumbs for clusters:
#  (1) (n/2)^.5
#  (2) elbow method


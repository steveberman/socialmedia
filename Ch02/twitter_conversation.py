# Chap02-03/twitter_conversation.py
# network graph of conversation, from initial to replies
# creates directed acyclic graph
# predecessors:
#

import sys
import json
from operator import itemgetter
import networkx as nx

def usage():
    print("Usage:")
    print("python {} <filename>".format(sys.argv[0]))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    fname = sys.argv[1]
    graph = nx.DiGraph()

    with open(fname) as f:
        for line in f:
            tweet = json.loads(line)
            if 'id' in tweet:
                graph.add_node(tweet['id'], tweet=tweet['text'],
                               author=tweet['user']['screen_name'],
                created_at=tweet['created_at'])
                if tweet['in_reply_to_status_id']:
                    reply_to = tweet['in_reply_to_status_id']
                    # ignores replies to self (which are just multi-thread tweets)
                    if reply_to in graph and \
                            tweet['user']['screen_name'] != graph.node[reply_to]['author']:
                        graph.add_edge(tweet['in_reply_to_status_id'], tweet['id'])

    # Print some basic stats
    print(nx.info(graph))
    # Find most replied tweet
    # degree_iter iterates over (node, degree) tuples
    #   itemgetter is used to sort based on column 1 (the degree), in this case in decreasing order
    sorted_replied = sorted(graph.degree_iter(), key=itemgetter(1),
                            reverse=True)
    most_replied_id, replies = sorted_replied[0]
    print("Most replied tweet ({} replies):".format(replies))
    print(graph.node[most_replied_id])

    # Find longest conversation
    print("Longest discussion:")
    # built-in function of networkx, returns list of ids
    longest_path = nx.dag_longest_path(graph)
    for tweet_id in longest_path:
        node = graph.node[tweet_id]
        print("{} (by {} at {})".format(node['tweet'], node['author'], node['created_at']))

# usage:
#   python twitter_conversation.py <filename>
#      where filename would be a file of tweets, from a history or a stream
#      creates one node for each tweet

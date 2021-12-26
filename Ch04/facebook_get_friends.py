# Chap04/facebook_get_friends.py
# very imperfect way to get information from Facebook

import os
import facebook
import json

# NOTE: only retrieves friends that are users of the app
# so at first, would just provide friend count and empty friend list

if __name__ == '__main__':
    token = os.environ.get('FACEBOOK_TEMP_TOKEN')
    graph = facebook.GraphAPI(token)
    user = graph.get_object("me")
    friends = graph.get_connections(user["id"], "friends")
    print(json.dumps(friends, indent=4))
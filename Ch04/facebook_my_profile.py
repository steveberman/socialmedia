# Chap04/facebook_my_profile.py
# very basic pull from API
# requires a user access token to be set up  for a user / app

import os
import json
import facebook
from decouple import config

if __name__ == '__main__':
    # environ variable from an export
    #token = os.environ.get('FACEBOOK_TEMP_TOKEN')
    token = config('FACEBOOK_USER_ACCESS_TOKEN')
    graph = facebook.GraphAPI(token)
    # returns dictionary (?)
    profile = graph.get_object('me', fields='name,location')
    # include second level location information
    #    first level is attribute of user profile, second is attribute of Facebook page
    #      (with lat/long)
    #profile = graph.get_object('me', fields='name,location{location}')
    print(json.dumps(profile, indent=4))

# usage:
#   python facebook_my_profile.py


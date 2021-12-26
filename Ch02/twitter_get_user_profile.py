# twitter_get_user_profile.py
# single user profile

import json

from twitter_client import get_twitter_client

if __name__ == "__main__":
    client = get_twitter_client()
    profile = client.get_user(screen_name = "sberman8")
    print(json.dumps(profile._json, indent=4))
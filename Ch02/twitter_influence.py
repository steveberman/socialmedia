# Chap02-03/twitter_influence.py
# compare two different twitter users for number of followers, etc.
# predecessors:
#   (1) user jsonl files from twitter_get_user_profile_extended.py
#   (2) timeline files from twitter_get_user_timeline.py

import sys
import json

def usage():
    print("Usage:")
    print("python {} <username1> <username2>".format(sys.argv[0]))

if __name__ == '__main__':
    # validation for command line execution
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    screen_name1 = sys.argv[1]
    screen_name2 = sys.argv[2]

    dirname1 = f"users/{screen_name1}"
    dirname2 = f"users/{screen_name2}"

    # get followers for two different users
    followers_file1 = f"{dirname1}/followers.jsonl"
    followers_file2 = f"{dirname2}/followers.jsonl"
    with open(followers_file1) as f1, open(followers_file2) as f2:
        # reach adds all followers of followers (name of user + follower count)
        reach1 = []
        reach2 = []
        for line in f1:
            profile = json.loads(line)
            reach1.append((profile['screen_name'], profile['followers_count']))

        for line in f2:
            profile = json.loads(line)
            reach2.append((profile['screen_name'], profile['followers_count']))

    profile_file1 = f"{dirname1}/user_profile.json"
    profile_file2 = f"{dirname2}/user_profile.json"
    with open(profile_file1) as f1, open(profile_file2) as f2:
        profile1 = json.load(f1)
        profile2 = json.load(f2)
        followers1 = profile1['followers_count']
        followers2 = profile2['followers_count']
        tweets1 = profile1['statuses_count']
        tweets2 = profile2['statuses_count']
        sum_reach1 = sum([x[1] for x in reach1])
        sum_reach2 = sum([x[1] for x in reach2])
        avg_followers1 = round(sum_reach1 / followers1, 2)
        avg_followers2 = round(sum_reach2 / followers2, 2)

        timeline_file1 = f"user_timeline_{screen_name1}.jsonl"
        timeline_file2 = f"user_timeline_{screen_name2}.jsonl"
        with open(timeline_file1) as f1, open(timeline_file2) as f2:
            favorite_count1, retweet_count1 = [], []
            favorite_count2, retweet_count2 = [], []
            for line in f1:
                tweet = json.loads(line)
                favorite_count1.append(tweet['favorite_count'])
                retweet_count1.append(tweet['retweet_count'])
            for line in f2:
                tweet = json.loads(line)
                favorite_count2.append(tweet['favorite_count'])
                retweet_count2.append(tweet['retweet_count'])

            avg_favorite1 = round(sum(favorite_count1) / tweets1, 2)
            avg_favorite2 = round(sum(favorite_count2) / tweets2, 2)
            avg_retweet1 = round(sum(retweet_count1) / tweets1, 2)
            avg_retweet2 = round(sum(retweet_count2) / tweets2, 2)
            favorite_per_user1 = round(sum(favorite_count1) / followers1, 2)
            favorite_per_user2 = round(sum(favorite_count2) / followers2, 2)
            retweet_per_user1 = round(sum(retweet_count1) / followers1, 2)
            retweet_per_user2 = round(sum(retweet_count2) / followers2, 2)
            print("----- Stats {} -----".format(screen_name1))
            print("{} followers".format(followers1))
            print("{} users reached by 1-degree connections".format(sum_reach1))
            print("Average number of followers for {}'s followers: {}".format(screen_name1, avg_followers1))
            print("Favorited {} times ({} per tweet, {} per user)".format(sum(favorite_count1), avg_favorite1,
                                                                          favorite_per_user1))
            print("Retweeted {} times ({} per tweet, {} per user)".format(sum(retweet_count1), avg_retweet1,
                                                                          retweet_per_user1))
            print("----- Stats {} -----".format(screen_name2))
            print("{} followers".format(followers2))
            print("{} users reached by 1-degree connections".format(sum_reach2))
            print("Average number of followers for {}'s followers: {}".format(screen_name2, avg_followers2))
            print("Favorited {} times ({} per tweet, {} per user)".format(sum(favorite_count2), avg_favorite2,
            favorite_per_user2))
            print("Retweeted {} times ({} per tweet, {} per user)".format(sum(retweet_count2), avg_retweet2,
                                                                          retweet_per_user2))

# usage:
#    python twitter_influence.py <username1> <username2>
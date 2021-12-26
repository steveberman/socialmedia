# twitter_map_batch.py
# IN PROGRESS: execute a series of programs to grab user timeline, then create geojson file from it
# by Steve Berman, last modified 22Dec2021

# programs to execute:
#   twitter_get_user_timeline.py  - get last tweets from a user
#   twitter_make_geojson.py

import subprocess
import os
import sys


def geojson_create(user_name):
    """ perform a series of programs to retrieve and map tweets

    :param user_name:
    :return:
    """
    # get twitter posts
    subprocess.run([sys.executable, "twitter_get_user_timeline.py", user_name])
    # convert into a geojson format
    str_timeline = f"user_timeline_{user_name}"
    subprocess.run([sys.executable, "twitter_make_geojson.py",
                    "--tweets", f"{str_timeline}.jsonl", "--geojson", f"{str_timeline}_geo.json"])
    # create map
    # NOTE: need to remove missing geometries prior to rendering
    subprocess.run([sys.executable, "twitter_map_clustered.py",
                    "--geojson", f"{str_timeline}_geo.json", "--map", f"{str_timeline}.html"])

    print("Process complete")


if __name__ == '__main__':
    # go through the batch
    #user_name = "JustinBieber"
    user_name = "marcwusinich"
    geojson_create(user_name)
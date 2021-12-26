# Chap02-03/twitter_map_basic.py
#   create simple map based on set of tweets
# predecessors:
#   geojson file created from tweets (or other)
#   (1) twitter_get_usertimeline.py to create jsonl file of tweets
#   (2) twitter_make_geojson.py to convert to json file with geo info
# make sure that some geo info actually in the tweets

from argparse import ArgumentParser
import folium
import json

def get_parser():
    parser = ArgumentParser()
    parser.add_argument('--geojson')
    parser.add_argument('--map')
    return parser

def is_blank_geo_file(geojson):
    """ TODO: test if a valid geojson specification has any data in it

    :param geojson: dictionary in geojson format
    :return: True if some location data in it, False if not
    :rtype: bool

    # last revised 22Dec2021
    """
    if geojson is None:
        return True

    try:
        if not geojson["features"]:
            return True
        else:
            return False
    except:
        # if errors, assume bad format
        return True

def make_map(geojson_file, map_file):
    # ENHANCE: center map around location of tweets
    tweet_map = folium.Map(location=[50, 5], zoom_start=5)
    try:
        geojson = json.load(open(geojson_file))
        geojson_layer = folium.GeoJson(geojson)  # name='geojson'
        print("File loaded")
        geojson_layer.add_to(tweet_map)
        tweet_map.save(map_file)
    except ValueError as e:
        print("Error in map creation.  Check that json file has a features list with some elements")
        print(e)
    except Exception as e:
        print(f"Error in map creation: {e}")

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    file_geo = args.geojson
    file_map = args.map

    # hardwired for IDE execution
    file_geo = "user_timeline_markwusinich_geo.json"
    file_map = "user_timeline_markwusinich.html"

    make_map(file_geo, file_map)

# usage:
#    python twitter_map_basic.py --geojson <geojsonfile> --map <outhtmlfile>

# examples:
# python twitter_map_basic.py --geojson rwc2015_final.geo.json \
#   --map rwc2015_final_tweets.html
# python twitter_map_basic.py --geojson user_timeline_markwusinich_geo.json
#   --map user_timeline_markwusinich.html


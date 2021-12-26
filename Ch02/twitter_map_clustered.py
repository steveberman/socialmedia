# Chap02-03/twitter_map_clustered.py
# show map with dense areas clustered
# predecessors:
#   geojson file created from tweets (or other)
#   (1) twitter_get_usertimeline.py to create jsonl file of tweets
#   (2) twitter_make_geojson.py to convert to json file with geo info

from argparse import ArgumentParser
import json
import folium
# added 22Dec2021
from folium.plugins import MarkerCluster

def get_parser():
    parser = ArgumentParser()
    parser.add_argument('--geojson')
    parser.add_argument('--map')
    return parser

def make_map(geojson_file, map_file):
    # NOTE: uses MarkerCluster object to group points
    # blank map
    tweet_map = folium.Map(location=[50, 5], zoom_start=5)
    # marker cluster layer (blank for now)
    marker_cluster = MarkerCluster().add_to(tweet_map)
    # geo layer
    geojson_layer = folium.GeoJson(open(geojson_file), name='geojson')
    # add clustering capability to geo layer
    geojson_layer.add_to(marker_cluster)
    tweet_map.save(map_file)

def make_map_2(geojson_file, map_file):
    """ more complicated version of map

    :param geojson_file:
    :param map_file:
    :return:
    """
    tweet_map = folium.Map(location=[50, 5], zoom_start=5)
    marker_cluster = folium.MarkerCluster().add_to(tweet_map)
    geodata = json.load(open(geojson_file))
    for tweet in geodata['features']:
        # coordinates in Marker are lat, long but in the geojson file
        #    they are long, lat, so must reverse
        tweet['geometry']['coordinates'].reverse()
        # add individual markers layer first with text, then clusters on top
        marker = folium.Marker(tweet['geometry']['coordinates'],
                               popup=tweet['properties']['text'])
        marker.add_to(marker_cluster)
        tweet_map.save(map_file)

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    make_map(args.geojson, args.map)

# usage:
# example:
#   twitter_map_clustered.py --geojson user_timeline_markwusinich_geo.json
#     --map user_timeline_markwusinich.html
# Chap02-03/twitter_make_geojson.py
# convert tweets into a GeoJSON file
# predecessors:
#   set of tweets from twitter_streaming.py or twitter_get_user_timeline.py

import json
from argparse import ArgumentParser

def get_parser():
    parser = ArgumentParser()
    parser.add_argument('--tweets')
    parser.add_argument('--geojson')
    return parser

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    # Read tweet collection and build geo data structure
    with open(args.tweets, 'r') as f:
        geo_data = {
            "type": "FeatureCollection",
            "features": []
        }
        for line in f:
            tweet = json.loads(line)
            try:
                if tweet['coordinates']:
                    geo_json_feature = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": tweet['coordinates']['coordinates']
                        },
                        "properties": {
                            "text": tweet['text'],
                            "created_at": tweet['created_at']
                        }
                    }
                    geo_data['features'].append(geo_json_feature)
            except KeyError:
                # Skip if json doc is not a tweet (errors, etc.)
                continue

        # Save geo data
        with open(args.geojson, 'w') as fout:
            fout.write(json.dumps(geo_data, indent=4))

# usage:
#   python twitter_make_geojson.py \
#   --tweets stream__RWC2015__RWCFinal_Rugby.jsonl \
#   --geojson rwc2015_final.geo.json

# where the first filename is a file with tweets and the geojson param stores
#    the geolocation info

# example:
# python twitter_make_geojson.py --tweets user_timeline_johnlucker.jsonl --geojson
#  user_timeline_johnlucker_geo.json

# each tweet loaded as a feature in the collection

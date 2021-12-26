# Chap04/facebook_get_page_info.py
# grab information from a specific facebook page
# predecessors: none

import os
import json
import facebook
from argparse import ArgumentParser
from decouple import config

def get_parser():
    parser = ArgumentParser()
    parser.add_argument('--page')
    return parser

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    token = config('FACEBOOK_USER_ACCESS_TOKEN')

    fields = ['id', 'name', 'about', 'likes',
        'website', 'link']

    fields = ','.join(fields)
    graph = facebook.GraphAPI(token)
    page = graph.get_object(args.page, fields=fields)
    print(json.dumps(page, indent=4))

# usage:
#   python facebook_get_page_info.py --page <pagename>
# example:
#   python facebook_get_page_info.py --page PacktPub
# NOTE:  endpoint requires the 'pages_read_engagement' permission
#   or the 'Page Public Content Access' feature or the 'Page Public Metadata Access' feature.
#   App must undergo the app review process



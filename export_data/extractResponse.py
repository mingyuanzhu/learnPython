#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import exportmeta
import logging
import unittest

reload(sys)
sys.setdefaultencoding('utf-8')

console = logging.StreamHandler()
console.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s %(thread)d - %(message)s'))
logging.getLogger(__name__).addHandler(console)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def print_help():
    print """
1, this script tested under python V2.7

2, sudo pip install boto3

3, cat ~/.aws/config
[default]
region=ap-southeast-1

4, cat ~/.aws/credentials
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY

$ python exportresponse.py 123 response.json 123_response.csv
for search response "response.json", exports app_id: "123" to file "123_response.csv"
    """


def main(app_id, response_file, output_file):
    response = json.load(open(response_file, 'rb'))
    if 'result' not in response:
        return
    sources = []
    for result in response['result']:
        if 'im_name' not in result:
            continue
        source = {
            'a': app_id,
            'n': result['im_name']
        }
        sources.append(source)
    thread_num = 1
    num_limit = 10000
    exportmeta.get_all_metas(sources, thread_num, num_limit, output_file)


class TestGetMeta(unittest.TestCase):

    def test_0(self):
        sources = []
        for line in open('im_name.list', 'r'):
            if line[-1] == '\n':
                line = line[:-1]
            source = {
                'a': '1308',
                'n': line
            }
            sources.append(source)
        thread_num = 1
        num_limit = 10000
        output_file = "1308_new.csv"
        exportmeta.get_all_metas(sources, thread_num, num_limit, output_file)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print_help()
        sys.exit()

    i_app_id = sys.argv[1]
    i_response_file = sys.argv[2]
    i_output_file = sys.argv[3]

    main(i_app_id, i_response_file, i_output_file)
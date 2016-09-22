#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import boto3
from boto3.dynamodb import conditions
from threading import Thread, Lock

reload(sys)
sys.setdefaultencoding('utf-8')

console = logging.StreamHandler()
console.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s %(thread)d - %(message)s'))
logging.getLogger(__name__).addHandler(console)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GetImageListThread(Thread):

    key_index = 0
    keys_lock = Lock()
    sources_lock = Lock()

    def __init__(self, thread_id, keys, sources):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.keys = keys
        self.sources = sources
        self.dynamodb = boto3.resource('dynamodb')
        self.table_image = self.dynamodb.Table('staging_zhiwei_visearch_ireland_image')
        self.table_meta = self.dynamodb.Table('staging_zhiwei_visearch_ireland_meta')

    def run(self):
        logger.debug("start thread,thread_id:%d", self.thread_id)

        index_key = self.get_next_key()
        while index_key is not None:
            items = self.get_all_items_by_index(index_key)
            self.append_sources(items)
            index_key = self.get_next_key()

        logger.debug("end thread,thread_id:%d", self.thread_id)

    def append_sources(self, items):
        try:
            GetImageListThread.sources_lock.acquire()
            self.sources.extend(items)
        except:
            logger.exception("append_source error")
        finally:
            GetImageListThread.sources_lock.release()

    def get_next_key(self):
        try:
            GetImageListThread.keys_lock.acquire()
            if GetImageListThread.key_index >= len(self.keys):
                return None
            GetImageListThread.key_index += 1
            return self.keys[GetImageListThread.key_index - 1]
        except:
            logger.exception("get_next_key error")
            return None
        finally:
            GetImageListThread.keys_lock.release()

    def parse_query_image_response(self, response):
        if 'Items' in response:
            items = response['Items']
        else:
            items = []
        if 'LastEvaluatedKey' in response:
            last_evaluated_key = response['LastEvaluatedKey']
        else:
            last_evaluated_key = {}
        return items, last_evaluated_key

    def get_all_items_by_index(self, index_key):
        logger.debug("start get_all_items_by_index,index_key:%s", index_key)

        items = []
        response = self.table_image.query(
            # IndexName='app_id_hash-update_time-index',
            IndexName='app_id-all_images-index',
            Select='ALL_PROJECTED_ATTRIBUTES',
            ConsistentRead=False,
            ReturnConsumedCapacity='INDEXES',
            KeyConditionExpression=conditions.Key('a_h').eq(index_key)
        )

        new_items, last_evaluated_key = self.parse_query_image_response(response)
        items.extend(new_items)

        logger.debug("get items ok,index_key:%s items_count:%d", index_key, len(new_items))

        while len(last_evaluated_key) is not 0:
            response = self.table_image.query(
                # IndexName='app_id_hash-update_time-index',
                IndexName='app_id-all_images-index',
                Select='ALL_PROJECTED_ATTRIBUTES',
                ConsistentRead=False,
                ReturnConsumedCapacity='INDEXES',
                KeyConditionExpression=conditions.Key('a_h').eq(index_key),
                ExclusiveStartKey=last_evaluated_key
            )
            new_items, last_evaluated_key = self.parse_query_image_response(response)
            items.extend(new_items)

            logger.debug("get items ok,index_key:%s items_count:%d", index_key, len(new_items))

        logger.info("end get_all_items_by_index,index_key:%s items_count:%d", index_key, len(items))
        return items


class GetMetaThread(Thread):

    source_index = 0
    dest_num = 0
    sources_lock = Lock()
    dests_lock = Lock()

    def __init__(self, thread_id, sources, meta_fields, num_limit, fp):
        Thread.__init__(self)
        self.thread_id = thread_id
        self.sources = sources
        self.meta_fields = meta_fields
        self.num_limit = num_limit
        self.fp = fp
        self.dynamodb = boto3.resource('dynamodb')
        self.table_image = self.dynamodb.Table('staging_zhiwei_visearch_ireland_image')
        self.table_meta = self.dynamodb.Table('staging_zhiwei_visearch_ireland_meta')

    def run(self):
        logger.debug("start thread,thread_id:%d", self.thread_id)

        source_item = self.get_next_source()
        while source_item is not None:
            image_meta = self.get_image_meta(source_item['a'], source_item['n'])
            if image_meta is not None:
                logger.debug("get_image_meta ok,app_id:%s image_name:%s count:%d", image_meta['a'], image_meta['n'],
                             GetMetaThread.dest_num)
                self.append_dest(image_meta)
            source_item = self.get_next_source()

        logger.debug("end thread,thread_id:%d", self.thread_id)

    def output_meta(self, result):
        # print>>self.fp, result['a'],
        print>>self.fp, "%s" % result['n'],
        print>>self.fp, ",%s" % (result['l'] if 'l' in result else ''),
        print>>self.fp, ",%s" % (result['d'] if 'd' in result else ''),
        print>>self.fp, ",%s" % (result['k'] if 'k' in result else ''),
        print>>self.fp, ",%s" % (result['nd'] if 'nd' in result else ''),
        print>>self.fp, ",%s" % (result['nk'] if 'nk' in result else ''),
        for field in self.meta_fields.keys():
            print >>self.fp, ",\"%s\"" % (result['m'][field] if field in result['m'] else ''),
        print>>self.fp
        # self.fp.flush()

    def append_dest(self, image_meta):
        try:
            GetMetaThread.dests_lock.acquire()
            # if 'm' in image_meta:
            #     metas = image_meta['m']
            #     for key in metas.keys():
            #         self.meta_fields[key] = ''
            GetMetaThread.dest_num += 1
            self.output_meta(image_meta)
        except:
            logger.exception("append_dest error")
        finally:
            GetMetaThread.dests_lock.release()

    def get_next_source(self):
        try:
            GetMetaThread.dests_lock.acquire()
            if GetMetaThread.dest_num >= self.num_limit:
                return None
        except:
            logger.exception("get_next_source error,compare num_limit")
            return None
        finally:
            GetMetaThread.dests_lock.release()
        try:
            GetMetaThread.sources_lock.acquire()
            if GetMetaThread.source_index >= len(self.sources):
                return None
            GetMetaThread.source_index += 1
            return self.sources[GetMetaThread.source_index - 1]
        except:
            logger.exception("get_next_source error")
            return None
        finally:
            GetMetaThread.sources_lock.release()

    def get_image_id(self, app_id, image_name):
        response = self.table_image.query(
            Select='ALL_ATTRIBUTES',
            ConsistentRead=False,
            ReturnConsumedCapacity='INDEXES',
            KeyConditionExpression=conditions.Key('n').eq(image_name) & conditions.Key('a').eq(app_id)
        )
        if 'Items' not in response:
            logger.error("get_image_id response has no Items,app_id:%s image_name:%s", app_id, image_name)
            return None
        if len(response['Items']) == 0:
            logger.error("get_image_id response has 0 Items,app_id:%s image_name:%s", app_id, image_name)
            return None
        item = response['Items'][0]
        return item['i'], item['tx_j']

    def get_image_meta(self, app_id, image_name):
        image_id_trans_id = self.get_image_id(app_id, image_name)
        if image_id_trans_id is None:
            logger.error("get_image_meta no trans_id,app_id:%s image_name:%s", app_id, image_name)
            return None
        image_id, trans_id = image_id_trans_id
        response = self.table_meta.query(
            Select='ALL_ATTRIBUTES',
            ConsistentRead=False,
            ReturnConsumedCapacity='INDEXES',
            KeyConditionExpression=conditions.Key('i').eq(image_id) & conditions.Key('tx_j').eq(trans_id)
        )
        if 'Items' not in response:
            logger.error("get_image_meta response has no Items,app_id:%s image_name:%s", app_id, image_name)
            return None
        if len(response['Items']) == 0:
            logger.error("get_image_meta response has 0 Items,app_id:%s image_name:%s", app_id, image_name)
            return None
        return response['Items'][0]


def output_head(meta_fields, fp):
    print>>fp, "im_name,im_url,detect,keyword,nlp_detect, nlp_keyword",
    for field in meta_fields.keys():
        print>>fp, ",%s" % field,
    print>>fp


def get_all_items(app_id, thread_num):
    logger.debug("start get_all_items,app_id:%s", app_id)

    items = []
    index_keys = []
    for r in xrange(10):
        index_key = '%s_%d' % (str(app_id), r)
        index_keys.append(index_key)

    GetImageListThread.key_index = 0
    threads = []
    for thread_id in xrange(thread_num):
        thread = GetImageListThread(thread_id, index_keys, items)
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    logger.info("end get_all_items,app_id:%s items_count:%d", app_id, len(items))

    return items


def get_all_metas(sources, thread_num, num_limit, filename):
    logger.debug("start get_all_metas, sources_count:%d", len(sources))

    fp = open(filename, 'wb')
    meta_fields = {
        # "ImageBankURL5": "",
        # "SKU": "",
        # "ImageBankURL1": "",
        # "Width": "",
        # "BrandName": "",
        # "PrimaryEAN": "",
        # "Division": "",
        # "ParentInventoryID": "",
        "InventoryTitle": "",
        # "StockStatus": "",
        "Breadcrumb": "",
        # "CurrentPrice": "",
        # "Condition": "",
        # "RRP": "",
        # "SubCategory": "",
        "Category": ""
        # "Length": "",
        # "InventoryID": "",
        # "CategoryId": "",
        # "StockQuantity": "",
        # "WebCategory": "",
        # "Height": "",
        # "ProductURL": "",
        # "Manufacturer": "",
        # "Size": ""
    }
    GetMetaThread.source_index = 0
    GetMetaThread.dest_num = 0
    threads = []
    for thread_id in xrange(thread_num):
        thread = GetMetaThread(thread_id, sources, meta_fields, num_limit, fp)
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    output_head(meta_fields, fp)
    fp.close()

    logger.info("end get_all_metas, results_count:%d meta_fields_count:%d", GetMetaThread.dest_num, len(meta_fields))


def main(app_id, filename, thread_num, num_limit):
    logger.info("start,app_id:%s thread_num:%d", app_id, thread_num)
    sources = get_all_items(app_id, thread_num)
    get_all_metas(sources, thread_num, num_limit, filename)
    logger.info("end,app_id:%s thread_num:%d", app_id, thread_num)


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

$ python exportmeta.py 123 123_meta.csv
exports all metadata from app_id: "123" to file "123_meta.csv"

$ python exportmeta.py 123 123_meta.csv 10
export with 10 threads, default use 1 thread

$ python exportmeta.py 123 123_meta.csv 10 10000
export only 10000 images, default export all images
    """

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print_help()
        sys.exit()
    if sys.argv[1] == '-h':
        print_help()
        sys.exit()

    i_app_id = sys.argv[1]
    i_filename = sys.argv[2]
    if len(sys.argv) >= 4:
        i_thread_num = int(sys.argv[3])
    else:
        i_thread_num = 1
    if len(sys.argv) >= 5:
        i_num_limit = int(sys.argv[4])
    else:
        i_num_limit = 100000000

    main(i_app_id, i_filename, i_thread_num, i_num_limit)
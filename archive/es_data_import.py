#!/usr/bin/env python

import json 
import csv
import requests
import logging
import argparse
import sys

# ElasticSearch parameters
ES_HOST = '127.0.0.1'
ES_PORT = '9200'

# Lets make some logs!
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s')
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

def postIndex(index, data):
    s = requests.Session()

    r = s.post( "http://%s:%s/%s/doc" % 
              (ES_HOST, ES_PORT, index), 
              data=json.dumps(data))
    
    _logger.debug(r.text)
    return r

def putIndex(index, id, data):
    r = requests.put( "http://%s:%s/%s/doc/%s?op_type=create" % 
              (ES_HOST, ES_PORT, index, id), 
              data=json.dumps(data))
    
    _logger.debug(r.text)
    return r

def deleteDocument(index, id):
    r = requests.delete( "http://%s:%s/%s/doc/%s" % (ES_HOST, ES_PORT, index, id)) 
    return r

def search(index, search=None, fromdate=None, todate=None):
    query = {
        "query": {
            "bool": {
                "must": [],
                "must_not": [],
                "should": [
                    
                ]
            }
        },
        "from": 0,
        "size": 10,
        "sort": [],
        "aggs": {}
    }
    if search:
        query['query']['bool']['should'].append({
            "query_string": {
                "default_field": "_all",
                "query": search
            }
        })

    r = requests.get("http://%s:%s/%s/_search" % (ES_HOST, ES_PORT, index), data=json.dumps(query))
    _logger.debug(r.text)
    data = json.loads(r.text)
    return [d['_source'] for d in data['hits']['hits']]
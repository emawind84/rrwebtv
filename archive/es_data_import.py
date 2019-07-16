#!/usr/bin/env python

import json 
import csv
import requests
import logging
import argparse
import sys
from django.conf import settings

# ElasticSearch parameters
ES_HOST = settings.ES_HOST
ES_PORT = settings.ES_PORT

# Lets make some logs!
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s')
_logger = logging.getLogger(__name__)
_logger.setLevel(settings.LOGGING_LEVEL)

def postIndex(index, data):
    s = requests.Session()

    r = s.post( "http://%s:%s/%s/doc" % 
              (ES_HOST, ES_PORT, index), 
              data=json.dumps(data))
    
    _logger.debug(r.text)
    return r

def createDocument(index, id, data):
    r = requests.put( "http://%s:%s/%s/doc/%s?op_type=create" % 
              (ES_HOST, ES_PORT, index, id), 
              data=json.dumps(data))
    
    _logger.debug(r.text)
    return r

def createOrUpdateDocument(index, id, data):
    r = requests.put( "http://%s:%s/%s/doc/%s" % 
              (ES_HOST, ES_PORT, index, id), 
              data=json.dumps(data))
    
    _logger.debug(r.text)
    return r

def deleteDocument(index, id):
    r = requests.delete( "http://%s:%s/%s/doc/%s" % (ES_HOST, ES_PORT, index, id)) 
    return r

def searchDocuments(index, query):
    r = requests.get("http://%s:%s/%s/_search" % (ES_HOST, ES_PORT, index), data=json.dumps(query))
    _logger.debug(r.text)
    jsonResponse = json.loads(r.text)
    data = []; total = 0; took = 0
    if jsonResponse['hits']:
        data = [d['_source'] for d in jsonResponse['hits']['hits']]
        total = jsonResponse['hits']['total']
        took = jsonResponse['took'] / 1000

    return (data, total, took)
from archive.es_data_import import createOrUpdateDocument, deleteDocument, searchDocuments
from archive.models import Performance
from django.conf import settings
from dateutil.parser import parse
import re

def index(performance):
    try:
        createOrUpdateDocument(settings.ES_INDEX, performance.id, {
            'id': performance.id,
            'track': performance.track,
            'rally': performance.rally,
            'category': performance.category,
            'youtube_id': performance.youtube_id,
            'uploaded_at': performance.uploaded_at.strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            'pilot': performance.pilot,
            'stage_number': performance.stage_number,
            'car': performance.car,
            'time': performance.time,
            'team': performance.team,
            'note': performance.note,
            'featured': performance.featured
        })
    except:
        pass

def index_all():
    for performance in Performance.objects.all():
        index(performance)

def delete(performance):
    deleteDocument(settings.ES_INDEX, performance.id)
    performance.delete()

def search(search):
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
        "size": 20,
        "sort": [
            { "uploaded_at" : {"order" : "desc"}},
        ],
        "aggs": {}
    }
    if search:
        query['query']['bool']['should'].append({
            "query_string": {
                "default_field": "_all",
                "query": search
            }
        })
    documents, total, took = searchDocuments(settings.ES_INDEX, query)
    for d in documents:
        d['uploaded_at'] = parse(d['uploaded_at'])

    return documents, total, took

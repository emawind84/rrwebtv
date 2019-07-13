from archive.es_data_import import createOrUpdateDocument, deleteDocument, searchDocuments
from archive.models import Performance
from django.conf import settings
import re

def create(**args):
    performance = Performance(**args)
    performance.save()

    index(performance)

def index(performance):
    createOrUpdateDocument(settings.ES_INDEX, performance.id, {
        'id': performance.id,
        'track': performance.track,
        'rally': performance.rally,
        'category': performance.category,
        'youtube_id': performance.youtube_id,
        'uploaded_at': performance.uploaded_at.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        'pilot_nickname': performance.pilot_nickname,
        'stage_number': performance.stage_number,
        'car': performance.car,
        'time': performance.time,
        'team': performance.team,
        'note': performance.note
    })

def delete(performance):
    deleteDocument(settings.ES_INDEX, performance.id)
    performance.delete()

def search(**args):
    return  searchDocuments(settings.ES_INDEX, **args)
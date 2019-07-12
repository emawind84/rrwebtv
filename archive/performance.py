from archive.es_data_import import putIndex, deleteDocument
from archive.models import Performance
import re

def create(**args):
    performance = Performance(**args)
    performance.save()

    index(performance)

def index(performance):
    putIndex('rrwebtv', performance.id, {
        'id': performance.id,
        'track': performance.track,
        'rally': performance.rally,
        'category': performance.category,
        'youtube_id': performance.youtube_id,
        'uploaded_at': performance.uploaded_at.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        'pilot_name': performance.pilot_name,
        'pilot_nickname': performance.pilot_nickname,
        'stage_number': performance.stage_number,
        'car': performance.car,
        'time': performance.time
    })

def delete(performance):
    deleteDocument('rrwebtv', performance.id)
    performance.delete()
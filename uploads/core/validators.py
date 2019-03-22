import os
from django.core.exceptions import ValidationError
from django.conf import settings

def validate_replay_file(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = settings.REPLAY_VALID_EXT
    if not ext in valid_extensions:
        raise ValidationError('The file should be a replay or a valid video file.')

def validate_file_size(value):
    filesize = value.size
    
    if filesize > settings.UPLOAD_MAX_SIZE:
        raise ValidationError("The maximum file size that can be uploaded is 10MB.")
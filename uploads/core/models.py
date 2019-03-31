from django.db import models
from time import gmtime, strftime
from .validators import validate_file_size, validate_replay_file

def date_directory_path():
    return strftime("%Y-%m-%d", gmtime())

def replay_directory_path(instance, filename):
    return '{0}/{1}/replays/{2}'.format(date_directory_path(), instance.document.pilot_nickname, filename)

def skin_directory_path(instance, filename):
    return '{0}/{1}/skins/{2}'.format(date_directory_path(), instance.pilot_nickname, filename)

class Document(models.Model):
    note = models.CharField(max_length=255, blank=True)
    skin = models.FileField(upload_to=skin_directory_path, blank=True, null=True, validators=[validate_file_size])
    pilot_name = models.CharField(max_length=200, blank=True)
    pilot_nickname = models.CharField(max_length=200, blank=False)
    copilot_name = models.CharField(max_length=200, blank=True)
    copilot_nickname = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    gdpr_accept = models.BooleanField(blank=False)

    def __str__(self):
        return '{} - {}'.format(self.uploaded_at, self.pilot_name)

    class Meta:
        ordering = ('uploaded_at', 'pilot_name')

class Replay(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    replay = models.FileField(upload_to=replay_directory_path, blank=True, null=True, validators=[validate_file_size, validate_replay_file])

    def __str__(self):
        return self.replay.name
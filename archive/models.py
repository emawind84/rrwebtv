from django.db import models
from uploads.core.models import Replay

class Performance(models.Model):
    note = models.CharField(max_length=255, blank=True)
    pilot_nickname = models.CharField(max_length=200, blank=True)
    team = models.CharField(max_length=200, blank=True)
    rally = models.CharField(max_length=200, blank=True)
    track = models.CharField(max_length=200, blank=False)
    stage_number = models.CharField(max_length=200, blank=True)
    car = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=200, blank=True)
    time = models.CharField(max_length=200, blank=True)
    youtube_id = models.CharField(max_length=200, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    replay = models.OneToOneField(Replay, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.uploaded_at, self.track)
from django import forms
from archive.models import Performance

class PerformanceForm(forms.ModelForm):

    class Meta:
        model = Performance
        fields = ('track', 'youtube_id', 'car', 'time', 'category', 'pilot_nickname', 'team', 'rally', 'stage_number', 'note', 'replay')
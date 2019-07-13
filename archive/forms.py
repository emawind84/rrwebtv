from django import forms
from archive.models import Performance
from uploads.core.utils import parse_youtube_id, parse_car, parse_stage, parse_category, parse_rally

class PerformanceForm(forms.ModelForm):

    class Meta:
        model = Performance
        fields = ('track', 'youtube_id', 'car', 'time', 'category', 'pilot_nickname', 'team', 'rally', 'stage_number', 'note', 'replay')

    def clean_youtube_id(self):
        data = self.cleaned_data['youtube_id']
        return parse_youtube_id(data)

def initial_from_replay(replay):
    return {
        'replay': replay,
        'pilot_nickname': replay.document.pilot_nickname,
        'note': replay.document.note,
        'stage_number': parse_stage(replay.replay.name),
        'car': parse_car(replay.replay.name),
        'category': parse_category(replay.replay.name),
        'rally': parse_rally(replay.replay.name),
    }
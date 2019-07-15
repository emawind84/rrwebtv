from django import forms
from django.utils.translation import gettext_lazy as _
from archive.models import Performance
from uploads.core.utils import parse_youtube_id, parse_car, parse_stage, parse_category, parse_rally

class PerformanceForm(forms.ModelForm):

    class Meta:
        abstract = True
        model = Performance
        fields = ('track', 'youtube_id', 'car', 'time', 'category', 'pilot', 'team', 'rally', 'stage_number', 'note', 'replay', 'featured')

        labels = {
            'track': _('Track Name'),
            'youtube_id': _('YouTube URL or ID'),
            'car': _('Car'),
            'time': _('Time'),
            'category': _('Category'),
            'pilot': _('Pilot'),
            'team': _('Team'),
            'rally': _('Rally'),
            'stage_number': _('Stage (SS)'),
            'note': _('Comments'),
            'gdpr_accept': _('I accept that these information collected will be used for the only purpose of creating videos inherent RealRally.')
        }

    def clean_youtube_id(self):
        data = self.cleaned_data['youtube_id']
        return parse_youtube_id(data)

class PublicPerformanceForm(PerformanceForm):
    gdpr_accept = forms.BooleanField(required=True, label=_('I accept that these information collected will be used for the only purpose of creating videos inherent RealRally.'))

    class Meta(PerformanceForm.Meta):
        fields = ('track', 'youtube_id', 'car', 'time', 'category', 'pilot', 'team', 'rally', 'stage_number', 'note', 'gdpr_accept')

    def clean_gdpr_accept(self):
        gdpr_accept = self.cleaned_data.get('gdpr_accept')
        if not gdpr_accept:
            self.add_error('gdpr_accept', _("Please accept the terms."))

        return gdpr_accept

def initial_from_replay(replay):
    return {
        'replay': replay,
        'pilot': replay.document.pilot_nickname,
        'note': replay.document.note,
        'stage_number': parse_stage(replay.replay.name),
        'car': parse_car(replay.replay.name),
        'category': parse_category(replay.replay.name),
        'rally': parse_rally(replay.replay.name),
    }
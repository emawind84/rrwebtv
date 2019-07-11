from django import forms
from django.utils.translation import gettext_lazy as _
from uploads.core.models import Document, Replay
from material import Layout, Row

class DocumentForm(forms.ModelForm):
    note = forms.CharField(widget=forms.Textarea(attrs={'cols': 80}), required=False)
    replays = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True, 
    help_text=_('You can upload several replay files, make sure you upload only the original files, no other files are permitted.'))
    #field_order = ['label', 'category', 'username', 'password', 'confirm_password', 'ip', 'url', 'config', 'notes', 'groups']

    layout = Layout(
        Row('pilot_nickname', 'pilot_name'),
        Row('copilot_nickname', 'copilot_name'),
        'note', 'replays', 'skin', 'gdpr_accept',
    )
    
    class Meta:
        model = Document
        fields = ('pilot_nickname', 'pilot_name', 'copilot_nickname', 'copilot_name', 'note', 'replays', 'skin', 'gdpr_accept')
        help_texts = {
            'pilot_name': _('This name might be included on videos and other resources online, make sure you read the terms.'),
            'copilot_name': _('This name might be included on videos and other resources online, make sure you read the terms.'),
            'skin': _('This is the skin of the car, please upload a compressed file with only the files you edited!'),
        }
        labels = {
            'pilot_name': _('Driver Real Name'),
            'pilot_nickname': _('Driver Nickname'),
            'copilot_name': _('Co-driver Real Name'),
            'copilot_nickname': _('Co-driver Nickname'),
            'note': 'Comments',
            'gdpr_accept': _('I accept that these information collected will be used for the only purpose of creating videos inherent RealRally.'),
        }

    def clean_gdpr_accept(self):
        gdpr_accept = self.cleaned_data.get('gdpr_accept')
        if not gdpr_accept:
            self.add_error('gdpr_accept', _("Please accept the terms."))

        return gdpr_accept

class ReplayForm(forms.ModelForm):
    edited = forms.BooleanField(required=False)

    class Meta:
        model = Replay
        fields = ('edited',)
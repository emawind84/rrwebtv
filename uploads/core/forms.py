from django import forms

from uploads.core.models import Document


class DocumentForm(forms.ModelForm):
    note = forms.CharField(widget=forms.Textarea(attrs={'cols': 80}), required=False)
    replays = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)
    #field_order = ['label', 'category', 'username', 'password', 'confirm_password', 'ip', 'url', 'config', 'notes', 'groups']

    class Meta:
        model = Document
        fields = ('pilot_nickname', 'pilot_name', 'copilot_nickname', 'copilot_name', 'note', 'replays', 'skin', 'gdpr_accept')
        help_texts = {
            'pilot_name': 'This name might be included on videos and other resources online, make sure you read the terms.',
            'copilot_name': 'This name might be included on videos and other resources online, make sure you read the terms.',
            'skin': 'This is the skin of the car, please upload a compressed file with only the files you edited!',
            'replay': 'This is the replay file, just put here one file, no compressed.',
        }
        labels = {
            'pilot_name': 'Driver Real Name',
            'pilot_nickname': 'Driver Nickname',
            'copilot_name': 'Co-driver Real Name',
            'copilot_nickname': 'Co-driver Nickname',
            'note': 'Comments',
            'gdpr_accept': 'I accept that these information collected will be used for the only purpose of creating videos inherent RealRally.',
        }

    def clean_gdpr_accept(self):
        gdpr_accept = self.cleaned_data.get('gdpr_accept')
        if not gdpr_accept:
            self.add_error('gdpr_accept', "Please accept the terms.")

        return gdpr_accept
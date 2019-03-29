from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms.utils import ErrorList
from django.views import View

from uploads.core.models import Document, Replay
from uploads.core.forms import DocumentForm
from uploads.core import validators


def home(request):
    return render(request, 'core/home.html', {'video_url': settings.HOME_VIDEO_URL})

@login_required
def replays(request):
    documents = Document.objects.all()
    return render(request, 'core/replays.html', {'documents': documents})

@login_required
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'core/simple_upload.html')

def model_form_upload(request):
    if request.method == 'POST':
        pass
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {'form': form})

class ReplayUploadView(View):
    def get(self, request):
        form = DocumentForm()
        return render(request, 'core/model_form_upload.html', {'form': form})
    
    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)
        replay_is_invalid = False
        if form.is_valid():
            document = form.save()
            for uploadedFile in request.FILES.getlist('replays'):
                try:
                    self.handle_uploaded_replay(uploadedFile, document)
                except ValidationError as e:
                    errors = form._errors.setdefault("replays", ErrorList())
                    errors.append(e.message)
                    #messages.error(request, e.message)

            if form.is_valid():
                #form = DocumentForm()
                messages.success(request, 'Thank you, we will create awesomeness with your contribution!')
                return redirect(reverse('model_form_upload'))
        return render(request, 'core/model_form_upload.html', {'form': form})

    def handle_uploaded_replay(self, replay, document):
        validators.validate_file_size(replay)
        validators.validate_replay_file(replay)
        replay = Replay(replay=replay)
        replay.document = document
        replay.save()
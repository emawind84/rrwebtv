from datetime import datetime, timedelta, date
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
from django.db.models import Q
from django.utils.translation import gettext as _

from uploads.core.models import Document, Replay
from uploads.core.forms import DocumentForm, ReplayForm
from uploads.core import validators
from uploads.core.maker import Maker
from uploads.core.utils import parse_date

from archive.models import Performance

def home(request):
    #performances = Performance.objects.all().filter(featured=True)
    performances = Performance.objects.all()[:6]
    return render(request, 'core/home.html', {'performances': performances, 'video_url': settings.HOME_VIDEO_URL})

@login_required
def replays(request):
    documents = Document.objects.all()
    data = request.GET
    
    if data.get('search', '') != '':
        documents = documents.filter(
            Q(pilot_nickname__icontains=data.get('search')) | 
            Q(pilot_name__icontains=data.get('search')) |
            Q(note__icontains=data.get('search')) |
            Q(replay__replay__icontains=data.get('search'))
        )
    
    if not data.get('edited'):
        documents = documents.filter(replay__edited=False)
    
    start_date = parse_date(data.get('from_date'))
    end_date = parse_date(data.get('to_date'))
    if start_date:
        documents = documents.filter(uploaded_at__gte=start_date)
    if end_date:
        documents = documents.filter(uploaded_at__lte=end_date + timedelta(days=1))
    
    documents = documents.distinct()

    return render(request, 'core/replays.html', {'documents': documents, 'form': data})

class ReplayUploadView(View):
    def get(self, request):
        form = DocumentForm()
        return render(request, 'core/model_form_upload.html', {'form': form})
    
    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            replays = []
            for uploadedFile in request.FILES.getlist('replays'):
                try:
                    replays.append(self.handle_uploaded_replay(uploadedFile, document))
                except ValidationError as e:
                    errors = form._errors.setdefault("replays", ErrorList())
                    errors.append(e.message)
                    messages.error(request, e.message)

            if form.is_valid():
                document.save()
                form.save_m2m()
                for replay in replays:
                    replay.save(document)
                messages.success(request, _('Thank you, we will create awesomeness with your contribution!'))
                send_notification()
                return redirect(reverse('model_form_upload'))

        return render(request, 'core/model_form_upload.html', {'form': form})

    def handle_uploaded_replay(self, replay, document):
        validators.validate_file_size(replay)
        validators.validate_replay_file(replay)
        replay = Replay(replay=replay)
        replay.document = document
        return replay

@login_required
def edit_replay(request, replay_id):
    replay = get_object_or_404(Replay, id=replay_id)
    form = ReplayForm(instance=replay, data=request.POST)
    if form.is_valid():
        replay = form.save()
    return HttpResponse('')

def send_notification():
    maker = Maker()
    maker.send_async('rrwebtv_new_replay')
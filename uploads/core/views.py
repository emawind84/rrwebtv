from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from uploads.core.models import Document
from uploads.core.forms import DocumentForm


def home(request):
    return render(request, 'core/home.html')

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
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = DocumentForm()
            messages.success(request, 'Thank you, we will create awesomeness with your contribution!')
            return redirect(reverse('model_form_upload'))
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {'form': form})

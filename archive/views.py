import dateutil.parser
from datetime import timedelta, date
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from archive.models import Performance
from archive.forms import PerformanceForm, PublicPerformanceForm, initial_from_replay
from archive.performance import index, delete, search
from uploads.core.models import Replay
from uploads.core.utils import parse_date, parse_stage, parse_category, parse_car

def performances(request):
    data = request.GET

    start_date = parse_date(data.get('from_date'))
    end_date = parse_date(data.get('to_date'))
    
    performances = search(search=data.get('search'))

    return render(request, 'archive/performances.html', {'performances': performances, 'form': data})

@login_required
def new_performance(request, replay_id):
    if request.method != 'POST':
        replay = Replay.objects.get(id=replay_id)
        form = PerformanceForm(initial=initial_from_replay(replay))
    else:
        form = PerformanceForm(data=request.POST)
        if form.is_valid():
            performance = form.save()
            index(performance)
            return HttpResponseRedirect(reverse('archive:performances'))

    context = {'form': form, 'replay_id': replay_id}
    return render(request, 'archive/new_performance.html', context)

def new_public_video(request):
    if request.method != 'POST':
        form = PublicPerformanceForm()
    else:
        form = PublicPerformanceForm(data=request.POST)
        if form.is_valid():
            performance = form.save()
            index(performance)
            return HttpResponseRedirect(reverse('archive:performances'))

    context = {'form': form}
    return render(request, 'archive/new_public_video.html', context)

def performance(request, performance_id):
    performance = get_object_or_404(Performance, id=performance_id)

    context = {'performance': performance}
    return render(request, 'archive/performance.html', context)

@login_required
def edit_performance(request, performance_id):
    """Edit an existing secret."""
    performance = get_object_or_404(Performance, id=performance_id)

    if request.method != 'POST':
        form = PerformanceForm(instance=performance)
    else:
        form = PerformanceForm(instance=performance, data=request.POST)
        if form.is_valid():
            performance = form.save()
            index(performance)
            return HttpResponseRedirect(reverse('archive:performances'))

    context = {'performance': performance, 'form': form}
    return render(request, 'archive/edit_performance.html', context)

@login_required
def delete_performance(request, performance_id):
    performance = get_object_or_404(Performance, id=performance_id)

    if request.method == "POST":
        delete(performance)
        return HttpResponseRedirect(reverse('archive:performances'))
    
    context = {'performance': performance}
    return render(request, 'archive/delete_performance.html', context)

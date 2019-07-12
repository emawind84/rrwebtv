import dateutil.parser
from datetime import timedelta, date
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from archive.models import Performance
from archive.forms import PerformanceForm
from archive.es_data_import import putIndex, search
from archive.performance import index, delete
from uploads.core.models import Replay
from uploads.core.utils import parse_date, parse_stage, parse_category, parse_car

def performances(request):
    data = request.GET

    start_date = parse_date(data.get('from_date'))
    end_date = parse_date(data.get('to_date'))
    
    performances = search('rrwebtv', search=data.get('search'), fromdate=start_date, todate=end_date)

    return render(request, 'archive/performances.html', {'performances': performances, 'form': data})

def new_performance(request, replay_id=None):
    if request.method != 'POST':
        if replay_id:
            replay = Replay.objects.get(id=replay_id)
            form = PerformanceForm(initial={
                'replay': replay,
                'pilot_nickname': replay.document.pilot_nickname,
                'note': replay.document.note,
                'stage_number': parse_stage(replay.replay.name),
                'car': parse_car(replay.replay.name),
                'category': parse_category(replay.replay.name),
            })
        else:
            form = PerformanceForm()
    else:
        form = PerformanceForm(data=request.POST)
        if form.is_valid():
            performance = form.save(commit=False)
            performance.save()
            form.save_m2m()
            
            index(performance)

            return HttpResponseRedirect(reverse('archive:performances'))

    context = {'form': form}
    return render(request, 'archive/new_performance.html', context)

def performance(request, performance_id):
    performance = get_object_or_404(Performance, id=performance_id)

    context = {'performance': performance}
    return render(request, 'archive/performance.html', context)

@login_required
def delete_performance(request, performance_id):
    performance = get_object_or_404(Performance, id=performance_id)

    if request.method == "POST":
        delete(performance)
        return HttpResponseRedirect(reverse('archive:performances'))
    
    context = {'performance': performance}
    return render(request, 'archive/delete_performance.html', context)

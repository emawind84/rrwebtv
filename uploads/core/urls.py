from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import TemplateView

from uploads.core import views

urlpatterns = [

    url(r'^$', views.home, name='home'),

    url(r'^uploads/form/$', views.ReplayUploadView.as_view(), name='model_form_upload'),
    
    url(r'^replays/', views.replays, name='replays'),

    url(r'^edit_replay/(?P<replay_id>\d+)/$', views.edit_replay, name='edit_replay'),

]
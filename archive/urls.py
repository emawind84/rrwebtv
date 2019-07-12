from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from archive import views

urlpatterns = [
    
    path('performances/', views.performances, name="performances"),

    path('new_performance/', views.new_performance, name="new_performance"),

    path('new_performance/<int:replay_id>', views.new_performance, name="new_performance"),

    path('delete_performance/<int:performance_id>', views.delete_performance, name="delete_performance"),

    path('performances/<int:performance_id>', views.performance, name="performance"),
]

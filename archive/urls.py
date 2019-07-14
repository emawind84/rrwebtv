from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from archive import views

urlpatterns = [
    
    path('', views.performances, name="performances"),

    path('<int:performance_id>', views.performance, name="performance"),

    path('new_performance/<int:replay_id>', views.new_performance, name="new_performance"),

    path('edit_performance/<int:performance_id>', views.edit_performance, name="edit_performance"),

    path('delete_performance/<int:performance_id>', views.delete_performance, name="delete_performance"),

    path('share/', views.new_public_video, name="share"),

]

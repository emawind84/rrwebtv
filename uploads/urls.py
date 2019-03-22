from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from uploads.core import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^admin/', admin.site.urls),

    url(r'^uploads/form/$', views.model_form_upload, name='model_form_upload'),
    
    url(r'^replays/', views.replays, name='replays'),

    path('users/', include(('users.urls', 'users'), namespace='users')),

    path('accounts/', include('django.contrib.auth.urls')),

    path('auth/', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [

    path('', include('uploads.core.urls')),

    path('admin/', admin.site.urls),

    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),

    path('archive/', include(('archive.urls', 'archive'), namespace='archive')),

    path('users/', include(('users.urls', 'users'), namespace='users')),

    path('accounts/', include('django.contrib.auth.urls')),

    path('auth/', include('social_django.urls', namespace='social')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

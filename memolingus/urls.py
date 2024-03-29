from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns("",
    url(r"^$", direct_to_template, {"template": "homepage.html"}, name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),

    #parsapp
    url(r'^parse/$', 'parsapp.views.parse_input', name='parse'),
  	url(r'^words/(?P<status>\d{1})$', 'parsapp.views.word_view', name='words'),

)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
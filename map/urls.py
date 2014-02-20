from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'map.views.main'),
    url(r'^about/$', 'map.views.about'),
)

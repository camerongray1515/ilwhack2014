from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^get_tweet_meta/', 'data.views.get_tweet_meta'),
    url(r'^get_tweet/(?P<tweet_id>\d+)', 'data.views.get_tweet'),
)

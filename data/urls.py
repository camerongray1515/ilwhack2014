from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^get_tweet_meta/', 'data.views.get_tweet_meta'),
    url(r'^get_average_tweet_meta/', 'data.views.get_average_tweet_meta'),
    url(r'^get_tweet/(?P<tweet_id>\d+)', 'data.views.get_tweet'),
    url(r'^get_tag_cloud/(?P<region_code>\w+)', 'data.views.get_tag_cloud'),
)

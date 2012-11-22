# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('poll.views',
    url(r'^$', 'index', name='index'),
    url(r'^launch/$', 'launch', name='launch'),
    url(r'^poll/(.*)/(.*)/$', 'poll', name='poll'),
    url(r'^stop_interview/(.*)/(.*)/$', 'stop_interview', name='stop_interview'),
    url(r'^vote/(.*)/(.*)/(.*)/$', 'vote', name='vote'),
    url(r'^signup_results/(.*)/(.*)/$', 'signup_results', name='signup_results'),
    url(r'^show_results/(.*)/(.*)/$', 'show_results', name='show_results'),
)

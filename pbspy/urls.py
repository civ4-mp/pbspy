from django.conf import settings
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.urls import re_path

from pbspy import views

urlpatterns = [
    re_path(r'^$', views.game_list, name='game_list'),
    re_path(r'^game/(?P<pk>\d+)/$', views.game_detail, name='game_detail'),
    re_path(r'^game/(?P<game_id>\d+)/log/$', views.game_log, name='game_log'),
    re_path(r'^game/(?P<game_id>\d+)/manage/(?P<action>[^/]*)/?$', views.game_manage, name='game_manage'),
    re_path(r'^game/(?P<game_id>\d+)/update/$', views.game_update_manual, name='game_update_manual'),
    re_path(r'^game/(?P<game_id>\d+)/change/$', views.game_change, name='game_change'),
    re_path(r'^game/(?P<game_id>\d+)/change/(?P<action>[^/]*)/?$', views.game_change, name='game_change'),
    re_path(r'^game/(?P<game_id>\d+)/subscribe/$', views.game_subscribe, {'subscribe': True}, name='game_subscribe'),
    re_path(r'^game/(?P<game_id>\d+)/unsubscribe/$', views.game_subscribe, {'subscribe': False}, name='game_unsubscribe'),
    re_path(r'^game/(?P<game_id>\d+)/savefilter/$', views.game_save_filter, name='game_save_filter'),
    # Attention, filter_name can contain slashes, i.e. '01/04/2019i 11:53i p.m.'
    re_path(r'^game/(?P<game_id>\d+)/loadfilter/(?P<filter_name>.*)$', views.game_load_filter, name='game_load_filter'),
    re_path(r'^game/(?P<game_id>\d+)/removefilter/(?P<filter_name>.*)$', views.game_remove_filter, name='game_remove_filter'),
    re_path(r'^update$', views.game_update),
    re_path(r'^game/create/$', views.game_create, name='game_create'),
    re_path(r'^set_timezone$', views.set_timezone, name='set_timezone'),
    re_path(r'^accounts/', include('registration.backends.simple.urls')),
    re_path(r'^browserconfig.xml$', views.gen_browserconfig, name='gen_browserconfig'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

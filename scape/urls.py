from django.conf.urls import patterns, url

from scape import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^search/(?P<query>\w+)$', views.search, name='search'),
    url(r'^media/(?P<tag>\w+)/(?P<media_id>\w+)$', views.media, name='media'),
    url(r'^search_song/(?P<query>.+)$', views.search_song, name='search-song'),
    url(r'^attach_song$', views.attach_song, name='attach-song'),
    url(r'^(?P<keyword>\w+)$', views.detail, name='detail'),
)
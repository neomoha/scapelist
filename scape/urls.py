# -*- coding: utf-8 -*-

# This file is part of ScapeList.
#
# ScapeList is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ScapeList is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ScapeList.  If not, see <http://www.gnu.org/licenses/>.

# Written by Mohamed Sordo (@neomoha)
# Email: mohamed ^dot^ sordo ^at^ gmail ^dot^ com
# Website: http://msordo.weebly.com

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
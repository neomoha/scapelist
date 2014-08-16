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

from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from scape.models import Image, Keyword, Song, Annotation


import json
from instagram.client import InstagramAPI
CLIENT_ID = u"YOUR_INSTAGRAM_CLIENT_ID"
CLIENT_SECRET = u"YOUR_INSTAGRAM_CLIENT_SECRET"

import pyechonest.song as echo_song
import pyechonest.config as echo_config
echo_config.ECHO_NEST_API_KEY="YOUR_ECHO_NEST_API_KEY"

def unique( seq ):
    seen = set()
    for item in seq:
        if item not in seen:
            seen.add( item )
            yield item

def index(request, query=None):
    annotations = Annotation.objects.order_by('-id').values('keyword')
    keywords = [a['keyword'] for a in annotations]
    recent = []
    for keyword in list(unique(keywords))[:5]:
        k = Keyword.objects.get(pk=keyword)
        image = k.images.all()[:1][0]
        recent.append({'keyword': k.name, "instagram_id": image.instagram_id, "instagram_link": image.instagram_link, "thumbnail": image.thumbnail})    
    popular = []
    annotations = Annotation.objects.values('keyword').annotate(num_keywords=Count('keyword')).order_by('-num_keywords')
    keywords = [a['keyword'] for a in annotations[:5]]
    for keyword in keywords:
        k = Keyword.objects.get(pk=keyword)
        image = k.images.all()[:1][0]
        popular.append({'keyword': k.name, "instagram_id": image.instagram_id, "instagram_link": image.instagram_link, "thumbnail": image.thumbnail})
    context = {'recent': recent, 'popular': popular}
    
    return render(request, 'scape/index.html', context)

def detail(request, keyword):
    keyword = get_object_or_404(Keyword, name=keyword)
    images = keyword.images.all()
    results = [{"instagram_id": i.instagram_id, "instagram_link": i.instagram_link, "thumbnail": i.thumbnail} for i in images]
    return render(request, 'scape/detail.html', {'keyword': keyword, 'media': results})

def _get_tags(api, query):
    query = query.replace(" ", "")
    inst_tags = api.tag_search(query)
    if len(inst_tags[0]) > 0:
        return [(t.name, t.media_count) for t in inst_tags[0]]
    return []

def _get_images_by_tag(api, tag_name):
    media = api.tag_recent_media(tag_name=tag_name)
    images = []
    if len(media[0]) > 0:
        for item in media[0]:
            images.append({'standard_resolution': item.images['standard_resolution'].url,
                           'low_resolution': item.images['low_resolution'].url,
                           'thumbnail': item.images['thumbnail'].url,
                           'instagram_id': item.id, 'instagram_link': item.link, 'instagram_tags': [t.name for t in item.tags]})
    return images

def _get_image_by_id(api, media_id):
    item = api.media(media_id=media_id)
    image = None
    if item is not None:
        image = {'standard_resolution': item.images['standard_resolution'].url,
                   'low_resolution': item.images['low_resolution'].url,
                   'thumbnail': item.images['thumbnail'].url,
                   'instagram_id': item.id, 'instagram_link': item.link, 'instagram_tags': [t.name for t in item.tags]}
    return image

def search(request, query):
    api = InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    tags = _get_tags(api, query)
    images = []
    if len(tags) > 0:
        tag_name, tag_count = tags[0]
        images = _get_images_by_tag(api, tag_name)
    return HttpResponse(json.dumps(images), content_type="application/json")

def media(request, tag, media_id):
    keyword, created = Keyword.objects.get_or_create(name=tag)
    try:
        image = Image.objects.get(pk=media_id)
    except Image.DoesNotExist:
        api = InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        inst_image = _get_image_by_id(api, media_id)
        image = Image(instagram_id=inst_image['instagram_id'], instagram_link=inst_image['instagram_link'],
                standard_resolution=inst_image['standard_resolution'], low_resolution=inst_image['low_resolution'], thumbnail=inst_image['thumbnail'])
        image.save()
        for tag in inst_image['instagram_tags']:
            key, created = Keyword.objects.get_or_create(name=tag)
            key.images.add(image)
    annotated = "false"
    if request.user.is_authenticated():
        if Annotation.objects.filter(user=request.user, keyword=keyword):
            annotated = "true"
    playlist = []
    #annotations = Annotation.objects.filter(keyword=keyword).values('id', 'keyword', 'song').annotate(num_songs=Count('song')).order_by('-num_songs', 'id')
    
    annotations = Annotation.objects.filter(keyword=keyword).values('id', 'keyword', 'song')
    ann = {}
    for a in annotations:
        if not ann.has_key(a['song']):
            ann[a['song']] = [a, 0, a['id']]
        ann[a['song']][1]+=1
    sorted_annotations = sorted(ann.items(), key=lambda x: (x[1][1], -x[1][2]), reverse=True)
    results = [v[0] for k,v in sorted_annotations]
    for annotation in results:
        playlist.append(Song.objects.get(echonest_id=annotation['song']).spotify_trackid)
    #image.keywords.add(k)
    return render(request, 'scape/media.html', {'media': image, 'keyword': keyword, 'annotated': annotated, 'playlist': ",".join(playlist)})

def _get_spotify_trackid(song):
    ss_tracks = song.get_tracks('spotify-WW')
    if len(ss_tracks) == 0:
        return None
    track = ss_tracks[0]
    spotify_id = track["foreign_id"]
    spotify_trackid = spotify_id[spotify_id.rfind(':')+1:]
    return spotify_trackid

def search_song(request, query):
    ss_results = echo_song.search(combined=query, buckets=['id:spotify-WW'], limit=True, results=5)
    songs = []
    if len(ss_results) > 0:
        songs = [{"artist": s.artist_name, "title": s.title, "echonest_id": s.id, "spotify_trackid": _get_spotify_trackid(s)} for s in ss_results]
    return HttpResponse(json.dumps(songs), content_type="application/json")

@login_required
def attach_song(request):
    if request.is_ajax():
        song, created = Song.objects.get_or_create(echonest_id=request.POST["song_id"], spotify_trackid=request.POST["song_trackid"],
                                          defaults={'artist': request.POST["song_artist"], 'title': request.POST["song_title"]})
        image = Image.objects.get(instagram_id=request.POST['media_id'])
        keyword, created = Keyword.objects.get_or_create(name=request.POST['media_keyword'])
        annotation, created = Annotation.objects.get_or_create(user=request.user, image=image, song=song, keyword=keyword)
        playlist = []
        #annotations = Annotation.objects.filter(keyword=keyword).values('id', 'keyword', 'song').annotate(num_songs=Count('song')).order_by('-num_songs', 'id')
        annotations = Annotation.objects.filter(keyword=keyword).values('id', 'keyword', 'song')
        ann = {}
        for a in annotations:
            if not ann.has_key(a['song']):
                ann[a['song']] = [a, 0, a['id']]
            ann[a['song']][1]+=1
        sorted_annotations = sorted(ann.items(), key=lambda x: (x[1][1], -x[1][2]), reverse=True)
        results = [v[0] for k,v in sorted_annotations]
        for annotation in results:
            playlist.append(Song.objects.get(echonest_id=annotation['song']).spotify_trackid)
        #message = "Yes, AJAX! %s --> %s" % (song.echonest_id, image.instagram_id)
        message = ",".join(playlist)
    else:
        message = "Not Ajax"
    return HttpResponse(message)

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

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models

class Image(models.Model):
    instagram_id = models.CharField(max_length=50, primary_key=True)
    instagram_link = models.URLField()
    #instagram_tags = models.CharField(max_length=400)
    standard_resolution = models.URLField()
    low_resolution = models.URLField()
    thumbnail = models.URLField()

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.instagram_id

    class Meta:
        ordering = ('instagram_id',)

class Keyword(models.Model):
    name = models.CharField(max_length=255, unique=True)
    images = models.ManyToManyField(Image)

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
    
class Song(models.Model):
    echonest_id = models.CharField(max_length=50, primary_key=True)
    spotify_trackid = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    url = models.URLField()

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.artist+" "+self.title

    class Meta:
        ordering = ('artist','title')
        
class Annotation(models.Model):
    keyword = models.ForeignKey(Keyword)
    image = models.ForeignKey(Image)
    song = models.ForeignKey(Song)
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return "User %s has attached song %s-%s to image %s (keyword=%s)" % (self.user.username, self.song.artist, self.song.title,
                                                                             self.image.instagram_link, self.keyword.name)
    
    class Meta:
        unique_together = ("user", "keyword")
    
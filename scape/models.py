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
    
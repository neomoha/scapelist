from django.contrib import admin

# Register your models here.

from scape.models import Keyword, Image, Song

admin.site.register(Keyword)
admin.site.register(Image)
admin.site.register(Song)
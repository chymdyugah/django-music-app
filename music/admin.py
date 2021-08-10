from django.contrib import admin
from .models import Album, Song, Artist

# Register your models here.

admin.site.register(Album)  # registering the album model so that it can be manipulated from the admin site
admin.site.register(Song)  # registering the song model so that it can be manipulated from the admin site
admin.site.register(Artist)  # registering the artist model so that it can be manipulated from the admin site

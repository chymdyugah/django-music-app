from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse  # use this import for making redirection

# Create your models here.


class Artist(models.Model):
	artist_name = models.CharField(max_length=250)
	picture = models.FileField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	def get_absolute_url(self):
		return reverse('music:artist', kwargs={'pk': self.pk})  # when you create a new artist, it redirects you to the detail page of that artist.

	def __str__(self):
		return self.artist_name


class Album(models.Model):
	album_title = models.CharField(max_length=250)
	genre = models.CharField(max_length=250)
	album_logo = models.FileField()
	artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	def get_absolute_url(self):
		return reverse('music:detail', kwargs={'pk': self.pk})  # when you create a new album, it redirects you to the detail page of that album.

	def __str__(self):
		return self.album_title


class Song(models.Model):
	song_title = models.CharField(max_length=250)
	file = models.FileField()
	is_favourite = models.BooleanField(default=False)
	album = models.ForeignKey(Album, on_delete=models.CASCADE)

	def get_absolute_url(self):
		return reverse('music:index')

	def __str__(self):
		return self.song_title





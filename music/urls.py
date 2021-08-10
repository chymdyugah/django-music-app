from django.urls import path, include
from django.conf.urls import url  # no need to import this if you are using only path
from django.contrib.auth.decorators import login_required, permission_required  # these imports are used to restrict access to some pages
from . import views
from users.views import Login  # i imported this login view from the users app because i want this to be the first page users see if they are not logged in.

app_name = "music"  # this is called name spacing. It is used to reference non-hardcoded urls. check the views to see the usage

urlpatterns = [
	# /music/
	url(r'^$', Login.as_view(), name='login'),  # i can use the login directly now because i imported it and not the file

	# /music/home/
	url(r'^home/$', views.IndexView.as_view(), name='index'),  # OR path('', views.IndexView.as_view(), name='index') note the difference

	# /music/pk/
	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),  # make sure you use url instead, regular expressions makes the search better

	# music/album/add/
	url(r'album/add/$', views.CreateAlbum.as_view(), name='album-add'),

	# music/album/album primary key
	url(r'album/(?P<pk>[0-9]+)/$', views.UpdateAlbum.as_view(), name='album-update'),

	# music/album/album primary key/delete
	url(r'album/(?P<pk>[0-9]+)/delete/$', views.DeleteAlbum.as_view(), name='album-delete'),

	# music/register/
	#url(r'^register/$', views.UserFormView.as_view(), name='register'),

	# music/artist/add/
	url(r'^artist/add/$', views.CreateArtist.as_view(), name='artist-add'),

	# music/artist/artist primary key/update
	url(r'album/artist/(?P<pk>[0-9]+)/update$', views.UpdateArtist.as_view(), name='artist-update'),

	# music/artist/artist primary key/
	url(r'album/artist/(?P<pk>[0-9]+)$', views.ArtistView.as_view(), name='artist'),

	# music/song/add/
	url(r'^song/add/$', views.CreateSong.as_view(), name='song-add'),

	# music/song/add/
	url(r'^song/(?P<pk>[0-9]+)/delete$', views.DeleteSong.as_view(), name='song-delete'),

	# music/album primary key/favourite
	url(r'^(?P<pk>[0-9]+)/favourite/$', views.do_favourite, name='favourite'),

	# music/artists
	url(r'^artists/$', views.AllArtists.as_view(), name='all-artists'),
]


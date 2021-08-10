from django.http import Http404  # import this to raise 404 errors
from django.http import HttpResponse
from django.template import loader  # this is called when you want to use template loaders
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView  # use this whenever you want to make a form to create a new object, updateview edits an object and deleteview deletes an object in the db
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect  #redirect will help redirect you to a page after login
from django.contrib.auth import authenticate, login  # authenticate check your username and password if they are correct, login creates your session
from django.views.generic import View
from .models import Album, Song, Artist  # you need to import all models you will need here
from .forms import Userform  # you need to import all forms you will need here
from django.utils.decorators import method_decorator  # this import is for the restriction in the class
from django.contrib.auth.decorators import login_required

# Create your views here.
# function based views.... all commented out

"""def index(request):
	all_albums = Album.objects.all()
	# template = loader.get_template("music/index.html")  # import loader first and when you use render, you don't need this
	mycontext = {"all_albums": all_albums}  # used to send our albums to the template
	# return HttpResponse(template.render(mycontext, request))  # with render, you don't need this
	return render(request, "music/index.html", mycontext)


def detail(request, album_id):
	# the entire try...except block is good but it can be done by using the get_object_or_404 method
	# try:
	# 	album = Album.objects.get(pk=album_id)
	# # album = get_object_or_404(Album, pk=album_id)  # this is used with the get_object_or_404 import to raise the 404 error
	# except Album.DoesNotExist:
	# 	raise Http404("This album does not exist")
	album = get_object_or_404(Album, pk=album_id)
	return render(request, 'music/detail.html', {'album': album})
	# return HttpResponse("<h1>Details for album id:"+ album_id + "</h1>")


def do_favourite(request, album_id):
	album = get_object_or_404(Album, pk=album_id)
	try:
		selected_song = album.song_set.get(pk=request.POST['song'])
	except(KeyError, Song.DoesNotExist):
		render(request, 'music.detail.html', {"album": album, "error_message": "You have an error"})
	else:
		selected_song.is_favourite = True
		selected_song.save()
		render(request, 'music.detail.html', {"album": album})

"""
# class based view


@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
	template_name = 'music/index.html'
	context_object_name = 'all_albums'

	def get_queryset(self):
		return Album.objects.filter(owner=self.request.user)


@method_decorator(login_required, name='dispatch')
class DetailView(generic.DetailView):
	# this view naturally searches with the primary key so i had to change my search parameter in the urls file to pk
	# model = Album
	template_name = 'music/detail.html'
	# context_object_name = 'all_songs'

	def get_queryset(self):
		return Album.objects.filter(owner=self.request.user)  # i used this function to replace the model. instead of allowing it select from the entire album model, it now select from album records that match the filter


@method_decorator(login_required, name='dispatch')  # this is one way to restrict access. this method seems better and simpler but i cannot explain why
class ArtistView(generic.DetailView):
	# this view naturally searches with the primary key so i had to change my search parameter in the urls file to pk
	model = Artist
	template_name = 'music/artistsongs.html'


@method_decorator(login_required, name='dispatch')
class AllArtists(generic.ListView):
	template_name = 'music/artists.html'
	context_object_name = 'all_artists'

	def get_queryset(self):
		return Artist.objects.filter(owner=self.request.user)  # i allowed all the artists object because i want users to be able to see all artists everyone has created to avoid creating an artist multiple times


@method_decorator(login_required, name='dispatch')
class CreateAlbum(CreateView):
	model = Album
	fields = ['artist', 'album_title', 'genre', 'album_logo']
	# this view automatically creates a form with all the fields of the model but only the once listed above will show.

	def form_valid(self, form):  # this function allows me to assign the album to whoever added them
		form.instance.owner = self.request.user
		return super().form_valid(form)

	def get_form(self):
		form = super().get_form()
		form.fields['artist'].queryset = Artist.objects.filter(owner=self.request.user)
		return form


@method_decorator(login_required, name='dispatch')
class CreateSong(CreateView):
	model = Song
	fields = ['album', 'song_title', 'file', 'is_favourite']

	def get_form(self):  # this function is called to allow users add songs to only albums they created.
		form = super().get_form()
		form.fields['album'].queryset = Album.objects.filter(owner=self.request.user)
		return form


@method_decorator(login_required, name='dispatch')
class CreateArtist(CreateView):
	model = Artist
	fields = ['artist_name', 'picture']

	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super().form_valid(form)


class UpdateAlbum(UpdateView):
	model = Album
	fields = ['artist', 'album_title', 'genre', 'album_logo']


class UpdateArtist(UpdateView):
	model = Artist
	fields = ['artist_name', 'picture']


@method_decorator(login_required, name='dispatch')
class DeleteAlbum(DeleteView):
	model = Album
	success_url = reverse_lazy('music:index')


@method_decorator(login_required, name='dispatch')
class DeleteSong(DeleteView):
	model = Song
	success_url = reverse_lazy('music:index')


@login_required
def do_favourite(request, pk):
	album = get_object_or_404(Album, pk=pk)
	try:
		selected_song = album.song_set.get(pk=request.POST['song'])
	except(KeyError, Song.DoesNotExist):
		return render(request, 'music/detail.html', {
			'album': album,
			'error_message': 'You did not select any song',
		})
	else:
		if selected_song.is_favourite:
			selected_song.is_favourite = False
		else:
			selected_song.is_favourite = True

		selected_song.save()
		return render(request, 'music/detail.html', {'album': album})


@method_decorator(login_required, name='dispatch')
class DoFavourite(generic.DetailView):
	template_name = "music/detail.html"

	def get_queryset(self):
		return Album.objects.filter(owner=self.request.user)

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		try:
			selected_song = context['album'].song_set.get(pk=self.request.POST['song'])
		except(KeyError, Song.DoesNotExist):
			context['error_message'] = "You did not select any song."
		else:
			if selected_song.is_favourite:
				selected_song.is_favourite = False
			else:
				selected_song.is_favourite = True

			selected_song.save()

		return context


# i didn't use this.... transferred to the users app
""" class UserFormView(View):
	form_class = Userform
	template_name = 'music/registration.html'

	# display blank form on on request
	def get(self, request):
		form = self.form_class(None)  # none in parentheses because you want an empty form
		return render(request, self.template_name, {'form': form})

	# process form on post request
	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			user = form.save(commit=False)  # this does not actually save it to the database

			# cleaned data.(just so that our data has a universal format)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)  # this is the method to use to change password
			user.save()

			# returns user object if the inputs are correct
			user = authenticate(username=username, password=password)

			if user is not None:

				if user.is_active:
					login(request, user)  # this logs in the user and creates session
					return redirect('music:index')

		return render(request, self.template_name, {'form': form}) """

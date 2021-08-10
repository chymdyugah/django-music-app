from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView  # this view is embedded in django, it creates the login function and session, it only needs a template in order to display the login form
from django.contrib.auth import logout, authenticate, login
from django.views.generic import View
from .forms import Userform  # you need to import all forms you will need here


# Create your views here.

class Login(LoginView):
	template_name = 'users/login.html'


def Logout(request):
	logout(request)

	return redirect('users:index')


class UserFormView(View):
	form_class = Userform
	template_name = 'users/registration.html'

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

		return render(request, self.template_name, {'form': form})


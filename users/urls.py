from django.conf.urls import url  # no need to import this if you are using only path
from django.contrib.auth.views import LoginView
from . import views

app_name = "users"  # this is called name spacing. It is used to reference non-hardcoded urls. check the views to see the usage

urlpatterns = [
	# /users/login
	url(r'^login/$', views.Login.as_view(), name='index'),  # OR path('', LoginView, name='index') note the difference

	# /users/logout
	url(r'^logout/$', views.Logout, name='logout'),

	# user/register/
	url(r'^register/$', views.UserFormView.as_view(), name='register'),
]


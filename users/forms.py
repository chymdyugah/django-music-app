from django.contrib.auth.models import User  # this is how to import follow come models like user and groups
from django import forms

class Userform(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))  # the widget attribute makes the input to be encoded into asterisks

	class Meta:
		model = User  # we didnt write this model ourselves, it came with django. you will see the model in the django admin panel
		fields = ['first_name', 'last_name', 'username', 'password', 'email']




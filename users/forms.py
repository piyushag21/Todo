from django.contrib.auth.forms import UserCreationForm
from .models import User,Todo
from django.contrib.auth import authenticate
from django import forms
from django.forms import ModelForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)
 
	class Meta:
		model = User
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")

class TodoForm(forms.ModelForm):
    title= forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Add new task...'}))
    class Meta:
        model = Todo
        fields = ['title','status']
	

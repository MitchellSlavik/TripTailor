from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Traveler
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class TravelerProfileForm(forms.ModelForm):
    class Meta:
        model = Traveler
        fields = ()

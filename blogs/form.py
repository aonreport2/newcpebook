from django.contrib.auth.models import User
from  django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class signUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    password1 = forms.CharField(max_length=100)
    class Meta:
        model =User
        fields = ('first_name','last_name','username','password1','password2')

class UserProfileForm(forms.ModelForm):
    class Meta :
        model = UserProfile
        fields = ('std','edu','cpenumber','nickname','count')




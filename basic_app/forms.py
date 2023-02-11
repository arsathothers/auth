from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo

# Below is the base form which we are going to use for form fill ups
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ("portfolio_site", "profile_pic")
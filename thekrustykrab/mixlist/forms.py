from django import forms
from mixlist.models import Profile
from django.forms import ModelForm
from django.contrib.auth.models import User


class EditProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('about_me', 'location','profile_image')

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')


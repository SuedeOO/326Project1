from django import forms
from mixlist.models import Profile
from django.forms import ModelForm

class EditProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = (
            #'email',
            # 'first_name',
            # 'last_name',
            'about_me',
            'location',
            'user'
        )
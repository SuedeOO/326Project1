from django import forms
from mixlist.models import Profile, Comment, Mix
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class EditProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('about_me', 'location','profile_image')

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')
		
class CommentForm(forms.ModelForm) :
    class Meta:
        model = Comment
        fields = ('body',)

class EditMixForm(forms.Form):
    json = forms.CharField()

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta: 
        model = User
        fields = ('username', 'first_name','last_name','email','password1','password2')

    # def save(self, commit=True):
    #     user = super(RegistrationForm, self).save(commit=False)
    #     user.first_name = self.cleaned_data['first_name']
    #     user.last_name = self.cleaned_data['last_name']
    #     user.email = self.cleaned_data['email']

    #     if commit:
    #         user.save()
    #     return user 


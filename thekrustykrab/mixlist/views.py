from django.shortcuts import render
from django.views import generic
from .models import Mix

# Create your views here.
class MixView(generic.DetailView):
    model = Mix
    template_name = 'mix_detail.html'

class EditMixView(generic.DetailView):
    model = Mix
    template_name = 'editor_edit.html'
    
class UploadMixView(generic.TemplateView):
    template_name = 'editor_upload.html'

class ProfileView(generic.DetailView):
	model = Profile
	template_name = 'profile_template.html'
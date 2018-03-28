from django.shortcuts import render
from django.views import generic
from .models import Mix, Profile

# Create your views here.
class MixView(generic.DetailView):
    model = Mix
    template_name = 'mix_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(MixView, self).get_context_data(**kwargs)
        context['playlist'] = ['this', 'is', 'array']
        return context


class EditMixView(generic.DetailView):
    model = Mix
    template_name = 'editor_edit.html'
    
class UploadMixView(generic.TemplateView):
    template_name = 'editor_upload.html'

class ProfileView(generic.DetailView):
	model = Profile
	template_name = 'profile_template.html'

class MainPageView(generic.TemplateView):
    #model = 
    template_name = 'main_page.html'
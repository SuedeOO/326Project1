from django.shortcuts import render
from django.views import generic
from .models import Mix

# Create your views here.
class MixView(generic.DetailView):
    model = Mix
    template_name = 'mix_detail.html'


class EditMixView(generic.DetailView):
	model = Mix
	template_name = 'mix_edit.html'
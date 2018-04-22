from django.shortcuts import render, redirect
from django.views import generic
from .models import Mix, Profile, Follows, Track, PlaylistMembership, ExternalLink
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.urls import reverse
from django.utils.text import slugify
from datetime import timedelta
from django.contrib.auth.forms import UserChangeForm 
from django.db.models.functions import Lower
from django.contrib.auth.models import User
from mixlist.forms import (
    EditProfileForm,
    UserForm,
    CommentForm,
    RegistrationForm
)

def Search(request):
    query = request.GET.get('inputQuery')
    if query:
        #gives returns split list of exact matches and contains
        r_exactP = Profile.objects.filter(user__username__exact=query)
        r_Profile = Profile.objects.filter(user__username__contains=query).order_by(Lower('user__username')).exclude(id__in=r_exactP)
        
        r_exactM = Mix.objects.filter(title__exact=query)
        r_Mixes = Mix.objects.filter(title__contains=query).order_by('-play_count').exclude(id__in=r_exactM)
    return render(request, 'search.html', {'q':query, 'r_P': r_Profile,'r_M':r_Mixes, 'r_EP':r_exactP, 'r_EM':r_exactM})

def SignUp(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/')

    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'signup.html', args)

# Create your views here.
class MixView(generic.DetailView):
    model = Mix
    template_name = 'mix_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(MixView, self).get_context_data(**kwargs)
        playlist = []
        for member in context['mix'].playlistmembership_set.select_related().prefetch_related().all():
            playlist.append({
                'id': member.track.id,
                'title': member.track.title,
                'extra_info': member.track.extra_info or '',
                'artist': member.track.artist,
                'time': member.time.total_seconds(),
                'time_str': str(member.time),
                'links': [model_to_dict(link, fields=('provider', 'url')) for link in member.track.links.all()]
            })
        context['playlist'] = playlist
        if not self.request.user.is_anonymous:
            context['favoriteMix'] = self.request.user.profile.favorites.filter(pk=context['mix'].id).exists
        return context

class LogInView(generic.TemplateView):
    template_name = 'login_signup.html'

class UploadMixView(generic.TemplateView):
    template_name = 'editor_upload.html'

# New upload views here
#from .forms import UploadMixModelForm
class CreateMixView(generic.CreateView):
    model = Mix
    template_name = 'mix_upload.html'
    fields = ('title', 'audio_file')

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        form.instance.uploader = self.request.user.profile
        form.instance.length = timedelta()
        form.save()
        return redirect('/edit/' + form.instance.slug)


class ProfileView(generic.DetailView):
    model = Profile
    template_name = 'profile_template.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['follows'] = Follows.objects.filter(owner__user=self.kwargs['pk'])
        bfollows = []
        for rel in Follows.objects.filter(follows__user=self.kwargs['pk']):
            bfollows.append(rel.owner)
        context['bfollows'] = bfollows
        context['mixs'] = Mix.objects.filter(uploader__user=self.kwargs['pk'])
        return context
	
class MainPageView(generic.TemplateView):
    #model = Mix
    template_name = 'main_page.html' #fill this
    
    def get_context_data(self, **kwargs):
     
     model = Mix   
     context = super(MainPageView, self).get_context_data(**kwargs)
     context['mixes'] = Mix.objects.all()[:3]
     return context    
	
class ChartsView(generic.ListView):
    model = Mix
    template_name = 'charts_template.html'
    queryset = Mix.objects.order_by('-play_count')[:5]


def edit_profile(request):
    if request.method == 'POST':
        profile_form = EditProfileForm(request.POST, instance = request.user.profile)
        user_form = UserForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save() 
            pk = request.user.pk
            pk = str(pk)
            return redirect('/profile/'+pk)
    else:
        profile_form = EditProfileForm(instance = request.user.profile)
        user_form=UserForm(instance = request.user)
        return render(request,'edit_profile.html', {'user_form': user_form,'profile_form': profile_form})


def follow(request, profile_id):
    user = request.user.profile
    profile = Profile.objects.get(id=profile_id)
    f = Follows(owner=user, follows=profile)
    f.save()
    return redirect("/profile/"+profile_id)

def unfollow(request, profile_id):
    user = request.user.profile
    profile = Profile.objects.get(id=profile_id)
    Follows.objects.filter(owner=user, follows=profile).delete()
    return redirect("/profile/"+profile_id)

def addFavorite(request, mix_id):
    user = request.user.profile
    if not user.favorites.filter(pk=mix_id).exists():
        user.favorites.add(mix_id)
    user.save()
    next = request.GET.get('next', '/')
    return redirect(next)


def removeFavorite(request, mix_id):
    user = request.user.profile
    user.favorites.remove(mix_id)
    user.save()
    next = request.GET.get('next', '/')
    return redirect(next)

def addrecentPlayed(request, mix_id):
    user = request.user.profile
    if not user.recentPlayed.filter(pk=mix_id).exists():
        user.recentPlayed.add(mix_id)
    user.save()
    return HttpResponse('')

def add_comment(request, slug):
    mix = Mix.objects.get(slug=slug)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
             comment = comment_form.save(commit=False)
             comment.mix = mix
             comment.user = request.user
             comment.save()
             return redirect("/mix/"+ slug)
    else:
        comment_form = CommentForm()
        return render(request, 'add_comment_to_mix.html', {'comment_form': comment_form})    

import json
import re
from .forms import EditMixForm
def edit_mix(request, slug):

    def get_track(tag):
        trackQuery = Track.objects.filter(title=tag['title'], artist=tag['artist'])
        if len(trackQuery) >= 1: 
            track = trackQuery[0]
            track = Track.objects.get(title=tag['title'], artist=tag['artist'])
            taggedLinks = tag['links'] #from input
            definedProviders = [link.provider for link in track.links.all()]            
            for link in taggedLinks:                
                prov = "OTHER"                
                if "soundcloud" in link: #m = re.match("(https?://)?soundcloud.com", link) perhaps use this later
                    prov = "SOUNDCLOUD"
                elif "spotify" in link:
                    prov = "SPOTIFY"
                elif "apple" in link or "itunes" in link:
                    prov = "APPLEMUSIC"
                elif "youtu" in link:
                    prov = "YOUTUBE" 
                
                if prov == "OTHER" or not prov in definedProviders:
                    ExternalLink.objects.create(track=track, provider=prov, url=link)                    
                
            return track
        else:
            newtrack = Track.objects.create(title=tag['title'], artist=tag['artist'], reference_count=0)
            links = tag['links']
            for link in links:                
                prov = "OTHER"                
                if "soundcloud" in link: #m = re.match("(https?://)?soundcloud.com", link) perhaps use this later
                    prov = "SOUNDCLOUD"
                elif "spotify" in link:
                    prov = "SPOTIFY"
                elif "apple" in link or "itunes" in link:
                    prov = "APPLEMUSIC"
                elif "youtu" in link:
                    prov = "YOUTUBE"                
                ExternalLink.objects.create(track=newtrack, provider=prov, url=link)
            return newtrack
            
    mix = Mix.objects.get(slug=slug)
    mixquery = Mix.objects.filter(slug=slug)
    if request.user == mix.uploader.user:
        if request.method=='POST':
            edit_mix_form = EditMixForm(request.POST)
            if edit_mix_form.is_valid():
                cd = edit_mix_form.cleaned_data
                data = json.loads(cd.get("json"))
                #TODO allow for editing title and author
                #mixquery.update(title=data['title'])
                #print(data['author'])
                print("author" + data['author'])
                mixquery.update(artist=data['author'], description=data['desc'])
                PlaylistMembership.objects.filter(mix=mix).delete()
                for tag in data['tags']:
                    track = get_track(tag)
                    time = timedelta(seconds=tag['time'])
                    PlaylistMembership.objects.create(mix=mix, track=track, time=time)
                return redirect("/mix/" + slug)            
        else:
            edit_mix_form = EditMixForm()
            return render(request, 'editor_edit.html', {'mix': mix, 'edit_mix_form': edit_mix_form, 'user':request.user}) 
    else:
        return redirect('upload-mix')
            
        
        
        

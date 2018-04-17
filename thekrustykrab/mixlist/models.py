from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    # email = models.EmailField(max_length=100)
    profile_image = models.FileField(blank=True, null=True)
    location = models.CharField(max_length = 25, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    #page of mixes
    favorites = models.ManyToManyField('Mix', blank=True)
    #page of liked profiles
    following = models.ManyToManyField('self', blank=True)
    def __str__(self):
        return self.user.get_username()
    #for admin view
    def full_name(self):
        return self.user.get_full_name()
    #for admin view
    def email(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])

#code to auto add profiles for users
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
#code to auto update profiles for user changes
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Mix(models.Model):
    '''
    Represents a Mix, an audio file uploaded with associated metadata tags
    '''
    audio_file = models.FileField() # TODO: Pass in a storage param
    title = models.CharField(max_length=80)
    artist = models.CharField(max_length=80, blank=True, null=True)
    image = models.FileField(blank=True, null=True)
    slug = models.SlugField() # title_of_song_with_underscores_as_spaces
    uploader = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="mixes")
    length = models.DurationField()
    upload_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    like_count = models.IntegerField(default=0)
    play_count = models.IntegerField(default=0)
    playlist = models.ManyToManyField('Track', through='PlaylistMembership')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('mix-detail', args=[str(self.slug)])
        
    def get_seconds(self):
        return self.length.seconds
        
class Track(models.Model):
    """
    A track, may be referenced by multiple Mixes
    """
    title = models.CharField(max_length = 100)
    artist = models.CharField(max_length = 50)
    extra_info = models.CharField(max_length = 100, blank=True, null=True) #remixer, etc.
    reference_count = models.IntegerField() #how mixes reference this track

    
    def get_links(self):        
        links = self.links.all()
        if links:
            combined = ""
            for link in links:
                combined += link.url + ";"
            return combined.rstrip(";")
        else:
            return ""
            
    def __str__(self):
        return str(self.artist) + " - " + str(self.title)


class ExternalLink(models.Model):
    """
    A link to where a track can be found elsewhere on the internet.
    """
    CHOICES = (
        ('SPOTIFY', 'Spotify'),
        ('SOUNDCLOUD','SoundCloud'),
        ('APPLEMUSIC','Apple Music'),
        ('YOUTUBE', 'YouTube'),
        ('OTHER', 'Other')
    )
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='links')
    provider = models.CharField(choices=CHOICES, max_length=50)
    url = models.URLField(max_length = 200)
    
    def __str__(self):
        return self.url


class PlaylistMembership(models.Model):
    '''
    Models the (many to many) relationship between a Mix and its tracks
    '''
    mix = models.ForeignKey(Mix, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    # the time in the mix that the track occurs
    time = models.DurationField() 

    def __str__(self):
        return str(self.mix.title) + '--' + str(self.track.title) + '@' + str(self.time)

class Follows(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='person_who_follows')
    follows = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='person_following')

class Comment(models.Model):
    mix = models.ForeignKey(Mix, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    def approve(selfself):
        self.approve = True
        self.save()

    def __str__(self):
        return self.body

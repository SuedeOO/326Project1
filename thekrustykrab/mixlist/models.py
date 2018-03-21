from django.db import models

# Create your models here.
class Mix(models.Model):
    '''
    Represents a Mix, an audio file uploaded with associated metadata tags
    '''
    audio_file = models.FileField() # TODO: Pass in a storage param
    title = models.CharField(max_length=80)
    slug = models.SlugField() # title_of_song_with_underscores_as_spaces
    # uploader = models.ForeignKey('User', on_delete=models.CASCADE)
    length = models.DurationField()
    upload_date = models.DateTimeField(auto_now_add=True)
    play_count = models.IntegerField()
    playlist = models.ManyToManyField('Track')

    def __str__(self):
        return self.title
        
        
class Track(models.Model):
    """
    A track, may be referenced by multiple Mixes
    """
    title = models.CharField(max_length = 100)
    artist = models.CharField(max_length = 50)
    extra_info = models.CharField(max_length = 100, blank=True, null=True) #remixer, etc.
    links = models.ManyToManyField('ExternalLink')
    reference_count = models.IntegerField() #how mixes reference this track
    
    def __str__(self):
        return str(self.artist) + " - " + str(self.title)
    
class ExternalLink(models.Model):
    """
    A link to where a track can be found elsewhere on the internet.
    """
    provider = models.CharField(max_length = 50)
    url = models.URLField(max_length = 200)
    
    def __str__(self):
        return self.url


from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #profile_image = models.ImageField() #TODO: param
    location = models.CharField(max_length = 25, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    following = models.ManyToManyField('self', blank=True, null=True)
    #favorites = models.ManyToManyField('Mix', blank=True)
    def __str__(self):
        return self.user.username
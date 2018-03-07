from django.db import models

# Create your models here.
class Mix(models.Model):
    '''
    Represents a Mix, an audio file uploaded with associated metadata tags
    '''
    audio_file = models.FileField()
    title = models.CharField(max_length=50)
    # uploader = models.ForeignKey('User', on_delete=models.CASCADE)
    length = models.DurationField()
    upload_date = models.DateTimeField()
    play_count = models.IntegerField()
    # playlist = ...

    def __str__(self):
        return self.title
        
        
class Track(models.Model):
    """
    A track, may be referenced by multiple Mixes
    """
    title = models.CharField(max_length = 100)
    artist = models.CharField(max_length = 50)
    extra_info = models.CharField(max_length = 100) #remixer, etc.
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
    
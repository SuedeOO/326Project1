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
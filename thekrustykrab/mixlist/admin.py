from django.contrib import admin
from .models import Mix, Track, ExternalLink

# Register your models here.
admin.site.register(Mix)
admin.site.register(Track)
admin.site.register(ExternalLink)

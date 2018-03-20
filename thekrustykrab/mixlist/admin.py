from django.contrib import admin
from .models import Mix, Track, ExternalLink, CustomUser

# Register your models here.
admin.site.register(Mix)
admin.site.register(Track)
admin.site.register(ExternalLink)
admin.site.register(CustomUser)
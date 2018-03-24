from django.contrib import admin
from .models import Mix, Track, ExternalLink, PlaylistMembership, Profile

# Register your models here.
admin.site.register(Track)
admin.site.register(ExternalLink)

class PlaylistMembershipInline(admin.TabularInline):
    model = PlaylistMembership
    extra = 1

@admin.register(Mix)
class MixAdmin(admin.ModelAdmin):
	inlines = (PlaylistMembershipInline,)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	#displays username, full name, and email when 
	#looking at profiles in admin view
    list_display = ('user', 'full_name', 'email')

    #separates different pieces for admin page
    fieldsets = (
    	(None, {
    		'fields': ('user', 'location', 'about_me')
    	}),
    	('Profile Lists', {
    		'fields': [('following', 'favorites')]
    	}),
    )
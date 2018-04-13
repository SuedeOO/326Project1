from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ExternalLink)

class PlaylistMembershipInline(admin.TabularInline):
    model = PlaylistMembership
    extra = 1

class ExternalLinkInline(admin.TabularInline):
	model = ExternalLink
	extra = 1

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
	inlines = (ExternalLinkInline,)
	extra = 1

@admin.register(Follows)
class FollowsAdmin(admin.ModelAdmin):
    list_display = ('owner', 'follows')

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
    		'fields': ('user', 'profile_image', 'location', 'about_me')
    	}),
    	('Profile Lists', {
    		'fields': [('following', 'favorites')]
    	}),
    )
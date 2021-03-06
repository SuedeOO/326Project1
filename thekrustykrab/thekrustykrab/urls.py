"""thekrustykrab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mixlist.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mix/<slug:slug>', MixView.as_view(), name='mix-detail'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
	path('upload', CreateMixView.as_view(), name='upload-mix'),
    path('edit/<slug:slug>', edit_mix, name='edit-mix'),
    path('', MainPageView.as_view(), name = 'main-page'),
    path('charts', ChartsView.as_view(), name = 'view-charts'),
    path('editprofile', edit_profile, name = 'edit-profile'),
    path('mix/<slug:slug>/addcomment', add_comment, name='add-comment'),
    path('search/', Search, name='Search')
]

# Use include() to add paths from the catalog application 
from django.urls import include

urlpatterns += [
    path('mixlist/', include('mixlist.urls')),
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', SignUp, name='signup'),
    path('profile/<profile_id>/follow', follow, name="follow"),
    path('profile/<profile_id>/unfollow', unfollow, name="unfollow"),
    path('mix/<mix_id>/addFavorite', addFavorite, name="addFavorite"),
    path('mix/<mix_id>/removeFavorite', removeFavorite, name="removeFavorite"),
    path('mix/<mix_id>/addrecentPlayed',addrecentPlayed, name="addrecentPlayed"),
    path('removeRecentPlayed',removeRecentPlayed,name="removeRecentPlayed"),
]

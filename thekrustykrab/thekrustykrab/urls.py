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
from mixlist.views import MixView, ProfileView, UploadMixView, EditMixView, MainPageView, ChartsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mix/<slug:slug>', MixView.as_view(), name='mix-detail'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
	path('upload', UploadMixView.as_view(), name='upload-mix'),
    path('edit/<slug:slug>', EditMixView.as_view(), name='edit-mix'),
    path('mainPage',MainPageView.as_view(), name = 'main-page'),
    path('charts', ChartsView.as_view(), name = 'view-charts')
]

# Use include() to add paths from the catalog application 
from django.urls import include

urlpatterns += [
    path('mixlist/', include('mixlist.urls')),
]

#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/mixlist/')),
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

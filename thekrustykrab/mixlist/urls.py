from django.urls import path
from . import views


urlpatterns = [
	path('upload', views.UploadMixView.as_view(), name='upload-mix'),
    path('edit/<int:pk>', views.EditMixView.as_view(), name='edit-mix'),
]
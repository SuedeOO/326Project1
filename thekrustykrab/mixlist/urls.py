from django.urls import path
from . import views


urlpatterns = [
    path('edit/<int:pk>', views.EditMixView.as_view(), name='edit-mix'),
]
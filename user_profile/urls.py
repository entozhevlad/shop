from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('user_profile', views.profile, name='profile'),
    path('edit_profile', views.edit, name='edit')
]
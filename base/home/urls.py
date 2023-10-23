from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.signUp, name='signup'),
    path('login/', views.logIn, name='login'),
    path('profile/', views.profileView, name='profile'),
    path('editprofile/', views.editProfileView, name='editprofile')
]
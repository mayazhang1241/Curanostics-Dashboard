from django.urls import path
from . import views
from .views import UserProfileView

urlpatterns = [
    path('', views.home, name='home'),  # Route for the homepage
    path('api/user-profiles/', UserProfileView.as_view(), name='user-profiles'),
]
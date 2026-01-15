from django.urls import path
from . import views
from .views import LandingAPI

urlpatterns = [
    path('index/', LandingAPI.as_view(), name='index'),
]

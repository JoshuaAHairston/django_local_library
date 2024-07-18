from django.urls import path
from . import views

# Use the name attribute here for your static html when linking with urls.
urlpatterns = [
    path('', views.index, name='index'),
]

from django.urls import path

from .views import ready

app_name = "httpapp"

urlpatterns = [
    path('ready/', ready, name='ready'),
]

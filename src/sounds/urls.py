from django.urls import path

from . import views

app_name = "sounds"
urlpatterns = [
    path("sound/", views.sound, name="sound"),
]



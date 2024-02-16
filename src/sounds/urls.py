from django.urls import path

from . import views
from .views import SoundGeneratorCreateView, SoundGeneratorUpdateView

app_name = "sounds"
urlpatterns = [
    path("sounds/", views.sounds, name="sounds"),
    path("sound/<int:soundid>", views.sound, name="sound"),
    path("generators/", views.generators, name="generators"),
    path("generator/<int:generatorid>", views.generator, name="generator"),
    path('generator/new/', SoundGeneratorCreateView.as_view(), name='generator_new'),
    path('generator/edit/<int:pk>', SoundGeneratorUpdateView.as_view(), name='generator_edit'),
]
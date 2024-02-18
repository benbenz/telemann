from django.urls import path , re_path

from . import views
from .views import SoundGeneratorCreateView, SoundGeneratorUpdateView 

app_name = "sounds"
urlpatterns = [
    path("generators/", views.generators, name="generators"),
    path("generator/<int:generatorid>", views.generator, name="generator"),
    path('generator/new/', SoundGeneratorCreateView.as_view(), name='generator_new'),
    path('generator/edit/<int:pk>', SoundGeneratorUpdateView.as_view(), name='generator_edit'),
    re_path(r"sounds/(?P<generatorid>\w+)?/?$", views.sounds, name="sounds"),
    path('sound/render/<int:generatorid>/',views.render_sound,name='render_sound'),
]
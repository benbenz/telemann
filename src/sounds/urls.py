from django.urls import path , re_path

from . import views
from .views import SoundSourceCreateView, SoundSourceUpdateView 

app_name = "sounds"
urlpatterns = [
    path("sources/", views.sources, name="sources"),
    path("source/<int:srcid>", views.source, name="source"),
    path('source/new/', SoundSourceCreateView.as_view(), name='source_new'),
    path('source/edit/<int:pk>', SoundSourceUpdateView.as_view(), name='source_edit'),
    re_path(r"(?P<srcid>\w+)?/?$", views.sounds, name="sounds"),
    path('render/<int:srcid>/',views.render_sound,name='render_sound'),
    path('analyze/<int:srcid>/',views.analyze_sound,name='analyze_sound'),
    path('capture/<int:srcid>/',views.capture_sound_image,name='capture_sound_image'),
]
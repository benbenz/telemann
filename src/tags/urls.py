from django.urls import path , re_path

from . import views

app_name = "sounds"
urlpatterns = [
    path("search", views.tags_search, name="search"),
    path("wudget", views.tags_widget, name="widget"),
]
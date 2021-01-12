from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:new_event>", views.home, name="new_event"),
    path("delete_event/<int:delete_event>", views.delete_event, name="delete_event"),
    path("download_csv", views.download_csv, name="download_csv"),
]

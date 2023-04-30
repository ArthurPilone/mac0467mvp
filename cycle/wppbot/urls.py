from django.urls import path

from . import views

urlpatterns = [
    path("msgin", views.index, name="index"),
]
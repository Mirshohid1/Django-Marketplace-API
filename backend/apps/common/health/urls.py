from django.urls import path

from .views import health_live, health_ready

urlpatterns = [
    path("live/", health_live),
    path("ready/", health_ready),
]

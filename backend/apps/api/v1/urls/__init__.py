from django.urls import include, path

urlpatterns = [
    path("auth/", include("api.v1.urls.auth")),
    path("notifications/", include("api.v1.urls.notifications")),
    path("catalog/", include("api.v1.urls.catalog")),
    path("health/", include("common.health.urls")),
]

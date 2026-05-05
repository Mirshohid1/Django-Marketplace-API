from django.urls import include, path

urlpatterns = [
    path("auth/", include("api.v1.urls.auth")),
    path("products/", include("api.v1.urls.products")),
    path("notifications/", include("api.v1.urls.notifications")),
    path("health/", include("common.health.urls")),
]

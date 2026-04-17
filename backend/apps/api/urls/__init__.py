from django.urls import include, path

urlpatterns = [
    path("auth/", include("api.urls.auth")),
    path("products/", include("api.urls.products")),
    path("notifications/", include("api.urls.notifications")),
]

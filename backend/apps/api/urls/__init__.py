from django.urls import path, include


urlpatterns = [
    path('auth/', include('api.urls.auth')),
    path('products/', include('api.urls.products')),
]
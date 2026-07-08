from catalog.views import ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("products", ProductViewSet, basename="catalog")

urlpatterns = router.urls

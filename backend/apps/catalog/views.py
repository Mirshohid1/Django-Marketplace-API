from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models.products import Product
from .serializers.product import ProductInputSerializer, ProductOutputSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action in (
            "create",
            "update",
            "partial_update",
        ):
            return ProductInputSerializer

        return ProductOutputSerializer

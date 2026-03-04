from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from django.db.models import Q
from .models import Category, Product
from .permissions import IsOwner, IsOwnerOrAdmin, IsAdminOrReadOnly, IsVerified
from .pagination import ProductCursorPagination
from .serializers import (
    CategorySerializer, CategoryCreateUpdateSerializer,
    ProductListSerializer, ProductDetailSerializer,
    ProductCreateUpdateSerializer
)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdminOrReadOnly()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return CategorySerializer
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return CategoryCreateUpdateSerializer
        return None


class ProductViewSet(ModelViewSet):
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_fields = ('category', 'status')
    search_fields = ('title',)
    ordering_fields = ('price', 'created_at')
    ordering = ('-created_at',)

    pagination_class = ProductCursorPagination

    def get_queryset(self):
        qs = Product.objects.select_related("category", "owner").order_by('-created_at')

        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:
                return qs
            else:
                return qs.filter(Q(status=Product.Status.APPROVED) | Q(owner=user))
        else:
            return qs.filter(Q(status=Product.Status.APPROVED))

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsVerified()]
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsVerified(), IsOwnerOrAdmin()]
        return []

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        if self.action == 'retrieve':
            return ProductDetailSerializer
        if self.action in ('create', 'update', 'partial_update'):
            return ProductCreateUpdateSerializer
        return None

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        instance.soft_delete()

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        product = self.get_object()
        product.approve()  # метод модели делает проверку и меняет статус
        return Response({"status": product.status}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        product = self.get_object()
        product.reject()
        return Response({"status": product.status}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def archive(self, request, pk=None):
        product = self.get_object()
        product.archive()
        return Response({"status": product.status}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def restore(self, request, pk=None):
        product = self.get_object()
        product.restore()
        return Response({"is_deleted": product.is_deleted}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def unarchive(self, request, pk=None):
        product = self.get_object()
        product.restore_from_archive()
        return Response({"status": product.status}, status=status.HTTP_200_OK)

from rest_framework import serializers
from users.serializers import UserOutPutSerializer

from ..models.catalogs import Brand, Category
from ..models.products import Product
from ..services.use_cases.products_create import ProductCreateService
from ..services.use_cases.products_update import ProductUpdateService
from .attributes import AttributeValueInputSerializer, AttributeValueOutputSerializer
from .brand import BrandSerializer
from .category import CategorySerializer
from .image import ProductImageInputSerializer, ProductImageOutputSerializer
from .variant import ProductVariantInputSerializer, ProductVariantOutputSerializer


class ProductOutputSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()
    owner = UserOutPutSerializer()

    attribute_values = AttributeValueOutputSerializer(
        many=True,
        read_only=True,
    )

    images = ProductImageOutputSerializer(
        many=True,
        read_only=True,
    )

    variants = ProductVariantOutputSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "slug",
            "title",
            "description",
            "status",
            "category",
            "brand",
            "owner",
            "attribute_values",
            "images",
            "variants",
            "created_at",
            "updated_at",
            "deleted_at",
        )


class ProductInputSerializer(serializers.Serializer):
    title = serializers.CharField()

    description = serializers.CharField()

    status = serializers.CharField()

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())

    attribute_values = AttributeValueInputSerializer(
        many=True,
        required=False,
    )

    images = ProductImageInputSerializer(
        many=True,
        required=False,
    )

    variants = ProductVariantInputSerializer(
        many=True,
        required=False,
    )

    def create(self, validated_data):
        variants = validated_data.pop("variants")
        attributes_data = validated_data.pop("attribute_values")
        images_data = validated_data.pop("images")

        return ProductCreateService.execute(
            product_data=validated_data,
            variants_data=variants,
            attributes_data=attributes_data,
            images_data=images_data,
        )

    def update(self, instance, validated_data):
        variants_data = validated_data.pop("variants")
        attributes_data = validated_data.pop("attribute_values")
        try:
            images_data = validated_data.pop("images")
        except KeyError:
            images_data = []

        return ProductUpdateService.execute(
            product=instance,
            product_data=validated_data,
            variants_data=variants_data,
            attributes_data=attributes_data,
            images_data=images_data,
        )

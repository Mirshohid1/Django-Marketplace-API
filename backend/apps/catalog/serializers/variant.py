from rest_framework import serializers

from ..models.products import ProductVariant
from ..services.use_cases.products_create import ProductVariantCreateService
from ..services.use_cases.products_update import ProductVariantUpdateService
from .attributes import (
    VariantAttributeValueInputSerializer,
    VariantAttributeValueOutputSerializer,
)
from .image import (
    ProductVariantImageInputSerializer,
    ProductVariantImageOutputSerializer,
)


class ProductVariantOutputSerializer(serializers.ModelSerializer):
    attribute_values = VariantAttributeValueOutputSerializer(
        many=True,
        read_only=True,
    )

    images = ProductVariantImageOutputSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = ProductVariant
        fields = (
            "id",
            "sku",
            "name",
            "description",
            "price",
            "attribute_values",
            "images",
            "created_at",
            "updated_at",
            "deleted_at",
        )


class ProductVariantInputSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)

    sku = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    attribute_values = VariantAttributeValueInputSerializer(
        many=True,
        required=False,
    )

    images = ProductVariantImageInputSerializer(
        many=True,
        required=False,
    )

    def create(self, validated_data):
        product = validated_data.pop("product")
        attributes_data = validated_data.pop("attribute_values")
        images_data = validated_data.pop("images")

        return ProductVariantCreateService.execute(
            product=product,
            variant_data=validated_data,
            attributes_data=attributes_data,
            images_data=images_data,
        )

    def update(self, instance, validated_data):
        attributes_data = validated_data.pop("attribute_values")
        images_data = validated_data.pop("images")

        return ProductVariantUpdateService.execute(
            variant=instance,
            variant_data=validated_data,
            attributes_data=attributes_data,
            images_data=images_data,
        )

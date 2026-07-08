from rest_framework import serializers

from ..models.images import ProductImage, ProductVariantImage


class ProductVariantImageOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantImage
        fields = (
            "id",
            "image",
            "created_at",
            "updated_at",
            "deleted_at",
        )


class ProductImageOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            "id",
            "image",
            "created_at",
            "updated_at",
            "deleted_at",
        )


class ProductImageInputSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)

    image = serializers.ImageField()


class ProductVariantImageInputSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)

    image = serializers.ImageField()

from rest_framework import serializers
from users.serializers import UserOutPutSerializer

from .models.attributes import (
    Attribute,
    AttributeValue,
    VariantAttributeValue,
)
from .models.catalogs import Brand, Category
from .models.images import ProductImage, ProductVariantImage
from .models.products import Product, ProductVariant
from .services.use_cases.products_create import (
    ProductCreateService,
    ProductVariantCreateService,
)
from .services.use_cases.products_update import (
    ProductUpdateService,
    ProductVariantUpdateService,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "slug",
            "parent",
            "name",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
        )


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "id",
            "slug",
            "name",
            "created_at",
            "updated_at",
            "deleted_at",
        )


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = (
            "id",
            "slug",
            "name",
            "type",
            "is_variant_only",
            "created_at",
            "updated_at",
            "deleted_at",
        )


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(required=False)

    class Meta:
        model = AttributeValue
        fields = (
            "id",
            "attribute",
            "value",
            "product",
            "created_at",
            "updated_at",
            "deleted_at",
        )


class VariantAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantAttributeValue
        fields = (
            "id",
            "attribute",
            "value",
            "variant",
            "created_at",
            "updated_at",
            "deleted_at",
        )


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            "id",
            "image",
            "product",
            "created_at",
            "updated_at",
            "deleted_at",
        )


class ProductVariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantImage
        fields = (
            "id",
            "image",
            "variant",
            "created_at",
            "updated_at",
            "deleted_at",
        )


class ProductVariantSerializer(serializers.ModelSerializer):
    attribute_values = VariantAttributeValueSerializer(many=True, required=False)
    images = ProductVariantImageSerializer(many=True, required=False)

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
            "product",
            "created_at",
            "updated_at",
            "deleted_at",
        )

    def create(self, validated_data):
        product = validated_data.get("product")
        attributes_data = validated_data.get("attribute_values")
        images_data = validated_data.get("images")

        return ProductVariantCreateService.execute(
            product=product,
            variant_data=validated_data,
            attributes_data=attributes_data,
            images_data=images_data,
        )

    def update(self, instance, validated_data):
        attributes_data = validated_data.get("attribute_values")
        images_data = validated_data.get("images")

        return ProductVariantUpdateService.execute(
            variant=instance,
            variant_data=validated_data,
            attributes_data=attributes_data,
            images_data=images_data,
        )


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, required=False)
    attribute_values = AttributeValueSerializer(many=True, required=False)
    images = ProductImageSerializer(many=True, required=False)
    category = CategorySerializer()
    brand = BrandSerializer()
    owner = UserOutPutSerializer()

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

    def create(self, validated_data):
        variants = validated_data.get("variants")
        attributes_data = validated_data.get("attribute_values")
        images_data = validated_data.get("images")

        return ProductCreateService.execute(
            product_data=validated_data,
            variants_data=variants,
            attributes_data=attributes_data,
            images_data=images_data,
        )

    def update(self, instance, validated_data):
        variants_data = validated_data.get("variants")
        attributes_data = validated_data.get("attribute_values")
        images_data = validated_data.get("images")

        return ProductUpdateService.execute(
            product=instance,
            product_data=validated_data,
            variants_data=variants_data,
            attributes_data=attributes_data,
            images_data=images_data,
        )

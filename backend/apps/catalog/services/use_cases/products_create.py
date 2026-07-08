from django.db import transaction

from catalog.models.attributes import (
    AttributeValue,
    VariantAttributeValue,
)
from catalog.models.images import (
    ProductImage,
    ProductVariantImage,
)
from catalog.models.products import (
    Product,
    ProductVariant,
)


class ProductVariantCreateService:
    @classmethod
    @transaction.atomic
    def execute(
        cls,
        *,
        product: Product,
        variant_data: dict,
        attributes_data: list[dict],
        images_data: list[dict] | None = None,
    ) -> ProductVariant:
        variant = ProductVariant.objects.create(
            product=product,
            **variant_data,
        )

        attribute_values = [
            VariantAttributeValue(
                variant=variant,
                **attribute_data,
            )
            for attribute_data in attributes_data
        ]

        VariantAttributeValue.objects.bulk_create(attribute_values)

        if images_data:
            images = [
                ProductVariantImage(variant=variant, **image_data)
                for image_data in images_data
            ]
            ProductVariantImage.objects.bulk_create(images)

        return variant


class ProductCreateService:
    @classmethod
    @transaction.atomic
    def execute(
        cls,
        *,
        product_data: dict,
        variants_data: list[dict],
        attributes_data: list[dict],
        images_data: list[dict] | None = None,
    ) -> Product:
        product = Product.objects.create(**product_data)

        if images_data:
            images = [
                ProductImage(
                    product=product,
                    **image_data,
                )
                for image_data in images_data
            ]
            ProductImage.objects.bulk_create(images)

        attribute_values = [
            AttributeValue(product=product, **attribute_data)
            for attribute_data in attributes_data
        ]

        AttributeValue.objects.bulk_create(attribute_values)

        for variant_data in variants_data:
            ProductVariantCreateService.execute(
                product=product,
                variant_data=variant_data["variant"],
                attributes_data=variant_data.get("attributes", []),
                images_data=variant_data.get("images", []),
            )

        return product

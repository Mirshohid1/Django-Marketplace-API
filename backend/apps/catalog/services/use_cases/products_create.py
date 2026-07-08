from django.db import transaction

from ..models.attributes import (
    VariantAttributeValue,
)
from ..models.images import (
    ProductImage,
    ProductVariantImage,
)
from ..models.products import (
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

        for variant_data in variants_data:
            ProductVariantCreateService.execute(
                product=product,
                variant_data=variant_data["variant"],
                attributes_data=variant_data.get("attributes", []),
                images_data=variant_data.get("images", []),
            )

        return product

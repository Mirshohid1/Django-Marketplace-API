from django.db import transaction

from catalog.models.attributes import AttributeValue, VariantAttributeValue
from catalog.models.images import ProductImage, ProductVariantImage
from catalog.models.products import Product, ProductVariant

from .base import sync_related_entities
from .products_create import ProductVariantCreateService


class ProductVariantUpdateService:

    @classmethod
    @transaction.atomic
    def execute(
        cls,
        *,
        variant: ProductVariant,
        variant_data: dict,
        attributes_data: list[dict],
        images_data: list[dict] | None = None,
    ) -> ProductVariant:

        existing_attributes = {
            attribute.id: attribute
            for attribute in variant.attribute_values.all()  # type: ignore
        }

        attributes_to_create = []
        attributes_to_update = []

        for incoming_attribute in attributes_data:
            attribute_id = incoming_attribute.get("id")

            if not attribute_id:
                attributes_to_create.append(
                    VariantAttributeValue(
                        variant=variant,
                        attribute=incoming_attribute["attribute"],
                        value=incoming_attribute["value"],
                    )
                )

                continue

            existing_attribute = existing_attributes.get(attribute_id)

            if not existing_attribute:
                continue

            changed = False

            if existing_attribute.value != incoming_attribute["value"]:
                existing_attribute.value = incoming_attribute["value"]
                changed = True

            if changed:
                attributes_to_update.append(existing_attribute)

        sync_related_entities(
            existing_objects=existing_attributes,
            incoming_data=attributes_data,
            objects_to_create=attributes_to_create,
            objects_to_update=attributes_to_update,
            update_fields=["value"],
            model_class=VariantAttributeValue,
        )

        if images_data is not None:
            existing_images_data = {
                image.id: image for image in variant.images.all()  # type: ignore
            }

            images_to_create = []
            images_to_update = []

            for incoming_image in images_data:
                image_id = incoming_image.get("id")

                if not image_id:
                    images_to_create.append(
                        ProductVariantImage(
                            variant=variant,
                            image=incoming_image["image"],
                        )
                    )

                    continue

                existing_image = existing_images_data.get(image_id)

                if not existing_image:
                    continue

                changed = False

                if existing_image.image != incoming_image["image"]:
                    existing_image.image = incoming_image["image"]
                    changed = True

                if changed:
                    images_to_update.append(existing_image)

            sync_related_entities(
                existing_objects=existing_images_data,
                incoming_data=images_data,
                objects_to_create=images_to_create,
                objects_to_update=images_to_update,
                update_fields=["image"],
                model_class=ProductVariantImage,
            )

        if images_data == []:
            ProductVariantImage.objects.filter(
                variant=variant,
            ).delete()

        fields_to_update = []

        for field, value in variant_data.items():

            if getattr(variant, field) != value:
                setattr(variant, field, value)
                fields_to_update.append(field)

        if fields_to_update:
            variant.save(update_fields=fields_to_update)

        return variant


class ProductUpdateService:
    @classmethod
    @transaction.atomic
    def execute(
        cls,
        *,
        product: Product,
        product_data: dict,
        variants_data: list[dict],
        attributes_data: list[dict],
        images_data: list[dict] | None = None,
    ) -> Product:
        existing_attributes = {
            attribute.id: attribute
            for attribute in product.attribute_values.all()  # type: ignore
        }

        attributes_to_create = []
        attributes_to_update = []

        for incoming_attribute in attributes_data:
            attribute_id = incoming_attribute.get("id")
            if not attribute_id:
                attributes_to_create.append(
                    AttributeValue(
                        product=product,
                        attribute=incoming_attribute["attribute"],
                        value=incoming_attribute["value"],
                    )
                )

                continue

            existing_attribute = existing_attributes.get(attribute_id)

            if not existing_attribute:
                continue

            changed = False

            if existing_attribute.value != incoming_attribute["value"]:
                existing_attribute.value = incoming_attribute["value"]
                changed = True

            if changed:
                attributes_to_update.append(existing_attribute)

        sync_related_entities(
            existing_objects=existing_attributes,
            incoming_data=attributes_data,
            objects_to_create=attributes_to_create,
            objects_to_update=attributes_to_update,
            update_fields=["value"],
            model_class=AttributeValue,
        )

        if images_data is not None:
            existing_images_data = {
                image.id: image for image in product.images.all()  # type: ignore
            }

            images_to_create = []
            images_to_update = []

            for incoming_image in images_data:
                image_id = incoming_image.get("id")
                if not image_id:
                    images_to_create.append(
                        ProductImage(
                            product=product,
                            image=incoming_image["image"],
                        )
                    )
                    continue

                existing_image = existing_images_data.get(image_id)

                if not existing_image:
                    continue

                changed = False

                if existing_image.image != incoming_image["image"]:
                    existing_image.image = incoming_image["image"]
                    changed = True

                if changed:
                    images_to_update.append(existing_image)

            sync_related_entities(
                existing_objects=existing_images_data,
                incoming_data=images_data,
                objects_to_create=images_to_create,
                objects_to_update=images_to_update,
                update_fields=["image"],
                model_class=ProductImage,
            )

        existing_variants = {
            variant.id: variant for variant in product.variants.all()  # type: ignore
        }

        incoming_variant_ids = set()

        for incoming_variant in variants_data:

            variant_id = incoming_variant.get("id")

            variant_data = {
                key: value
                for key, value in incoming_variant.items()
                if key
                not in {
                    "attribute_values",
                    "images",
                    "id",
                }
            }

            variant_attributes = incoming_variant.get("attribute_values", [])

            variant_images = incoming_variant.get("images", None)

            if not variant_id:
                ProductVariantCreateService.execute(
                    product=product,
                    variant_data=variant_data,
                    attributes_data=variant_attributes,
                    images_data=variant_images,
                )
                continue

            incoming_variant_ids.add(variant_id)

            existing_variant = existing_variants.get(variant_id)

            if not existing_variant:
                continue

            ProductVariantUpdateService.execute(
                variant=existing_variant,
                variant_data=variant_data,
                attributes_data=variant_attributes,
                images_data=variant_images,
            )

        variants_to_delete = set(existing_variants.keys()) - incoming_variant_ids

        if variants_to_delete:
            ProductVariant.objects.filter(id__in=variants_to_delete).delete()

        fields_to_update = []

        for field, value in product_data.items():
            if getattr(product, field) != value:
                setattr(product, field, value)
                fields_to_update.append(field)

        if fields_to_update:
            product.save(
                update_fields=fields_to_update,
            )

        return product

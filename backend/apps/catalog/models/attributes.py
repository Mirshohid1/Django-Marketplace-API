from common.models import BaseModel, SoftDeleteModel
from django.db import models

from .products import Product, ProductVariant


class AttributeType(models.TextChoices):
    TEXT = "text", "Text"
    INTEGER = "integer", "Integer"
    BOOLEAN = "boolean", "Boolean"


class Attribute(BaseModel, SoftDeleteModel):
    name = models.CharField(max_length=100)

    slug = models.SlugField(unique=True)

    type = models.CharField(
        max_length=20,
        choices=AttributeType.choices,
        default=AttributeType.TEXT,
    )

    is_variant_only = models.BooleanField(default=False)

    class Meta:
        db_table = "attributes"

    def __str__(self):
        return self.name


class AttributeValue(BaseModel, SoftDeleteModel):
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="values",
    )

    value = models.CharField(max_length=255)

    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="attribute_values"
    )

    class Meta:
        db_table = "attribute_values"

        unique_together = (("attribute", "value"),)

    def __str__(self):
        return f"{self.attribute}: {self.value}"


class VariantAttributeValue(BaseModel, SoftDeleteModel):
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="attribute_values",
    )

    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
    )

    value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "variant_attribute_values"

        unique_together = (("variant", "attribute"),)

    def __str__(self):
        return f"{self.variant.sku} -> {self.attribute.name}"

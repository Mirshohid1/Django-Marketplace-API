from common.models import BaseModel, SoftDeleteModel
from django.db import models

from ..services.path_generators import (
    product_image_upload_path,
    product_variant_upload_path,
)
from .products import Product, ProductVariant


class ProductImage(BaseModel, SoftDeleteModel):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="images"
    )
    image = models.ImageField(upload_to=product_image_upload_path)


class ProductVariantImage(BaseModel, SoftDeleteModel):
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.PROTECT, related_name="images"
    )
    image = models.ImageField(upload_to=product_variant_upload_path)

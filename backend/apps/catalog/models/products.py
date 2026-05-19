from typing import Any

from common.models import BaseModel, SoftDeleteModel
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.text import slugify
from users.models import User

from ..managers import ProductManager
from .catalogs import Brand, Category


class Product(BaseModel, SoftDeleteModel):

    class Status(models.TextChoices):
        DRAFT = "draft"
        PENDING = "pending"
        APPROVED = "approved"
        REJECTED = "rejected"
        ARCHIVED = "archived"

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products")

    title = models.CharField(max_length=155)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    description = models.TextField()

    status = models.CharField(
        choices=Status.choices, default=Status.DRAFT, max_length=10
    )

    objects = ProductManager()

    def is_editable(self) -> bool:
        return not self.is_deleted and self.status in {
            self.Status.DRAFT,
            self.Status.REJECTED,
        }

    def _generate_unique_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1

        while self.__class__.all_objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def clean(self) -> None:
        if self.title:
            self.title = " ".join(self.title.split())

        if self.description:
            self.description = " ".join(self.description.split())

        if self.title and len(self.title) < 5:
            raise ValidationError("Title must be at least 5 characters")

        if self.description and len(self.description) < 20:
            raise ValidationError("Description must be at least 20 characters")

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.slug:
            self.slug = self._generate_unique_slug()

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    class Meta:
        indexes = [
            models.Index(
                fields=["owner", "-created_at"],
                condition=Q(is_deleted=False),
                name="idx_product_owner",
            ),
            models.Index(
                fields=["category", "-created_at"],
                condition=Q(status="approved", is_deleted=False),
                name="idx_product_category",
            ),
            models.Index(
                fields=["-created_at"],
                condition=Q(status="approved", is_deleted=False),
                name="idx_product_feed",
            ),
            models.Index(fields=["status"]),
        ]


class ProductVariant(BaseModel, SoftDeleteModel):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="variants"
    )
    name = models.CharField(max_length=155)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    sku = models.CharField(
        max_length=64,
        unique=True,
        editable=False,
    )

    def __str__(self) -> str:
        return self.name

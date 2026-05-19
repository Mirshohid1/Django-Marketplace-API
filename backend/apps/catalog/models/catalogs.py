from common.models import BaseModel, SoftDeleteModel
from django.db import models


class Category(BaseModel, SoftDeleteModel):
    name = models.CharField(max_length=155)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Brand(BaseModel, SoftDeleteModel):
    name = models.CharField(max_length=155)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def __str__(self) -> str:
        return self.name

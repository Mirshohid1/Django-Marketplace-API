from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils.text import slugify
from users.models import User

from .managers import ProductManager, ProductQuerySet


class Category(models.Model):
    name = models.CharField(max_length=155)
    slug = models.SlugField(max_length=200, unique=True)

    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):

    class Status(models.TextChoices):
        DRAFT = "draft"
        PENDING = "pending"
        APPROVED = "approved"
        REJECTED = "rejected"
        ARCHIVED = "archived"

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")

    category = models.ForeignKey(
        "Category", on_delete=models.PROTECT, related_name="products"
    )

    title = models.CharField(max_length=155)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )

    is_deleted = models.BooleanField(default=False)

    status = models.CharField(
        choices=Status.choices, default=Status.DRAFT, max_length=10
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProductManager()
    all_objects = ProductQuerySet.as_manager()

    def is_editable(self):
        return not self.is_deleted and self.status in {
            self.Status.DRAFT,
            self.Status.REJECTED,
        }

    def approve(self):
        if self.status != self.Status.PENDING:
            raise ValidationError("Only pending products can be approved")

        self.status = self.Status.APPROVED
        self.save(update_fields=["status"])

    def reject(self):
        if self.status != self.Status.PENDING:
            raise ValidationError("Only pending products can be rejected")

        self.status = self.Status.REJECTED
        self.save(update_fields=["status"])

    def archive(self):
        if self.status != self.Status.APPROVED:
            raise ValidationError("Only approved products can be archived")

        self.status = self.Status.ARCHIVED
        self.save(update_fields=["status"])

    def restore_from_archive(self):
        if self.status != self.Status.ARCHIVED:
            raise ValidationError("Only archived products can be restored")

        self.status = self.Status.APPROVED
        self.save(update_fields=["status"])

    def soft_delete(self):
        if self.is_deleted:
            return

        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

    def restore(self):
        if not self.is_deleted:
            return

        self.is_deleted = False
        self.save(update_fields=["is_deleted"])

    def _generate_unique_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1

        while self.__class__.all_objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def clean(self):
        if self.title:
            self.title = " ".join(self.title.split())

        if self.description:
            self.description = " ".join(self.description.split())

        if self.title and len(self.title) < 5:
            raise ValidationError("Title must be at least 5 characters")

        if self.description and len(self.description) < 20:
            raise ValidationError("Description must be at least 20 characters")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()

        self.full_clean()
        super().save(*args, **kwargs)

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


class ProductVariant(models.Model):
    pass

from django.db import models
from django.db.models import Q
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=155)
    slug = models.SlugField(max_length=200, unique=True)

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children'
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft'
        PENDING = 'pending'
        APPROVED = 'approved'
        REJECTED = 'rejected'
        ARCHIVED = 'archived'


    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')

    title = models.CharField(max_length=155)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    is_deleted = models.BooleanField(default=False)
    status = models.CharField(choices=Status.choices, default=Status.DRAFT, max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(
                fields=['owner', '-created_at'],
                condition=Q(is_deleted=False),
                name='idx_product_owner'
            ),
            models.Index(
                fields=['category', '-created_at'],
                condition=Q(status='approved', is_deleted=False),
                name='idx_product_category'
            ),
            models.Index(
                fields=['-created_at'],
                condition=Q(status='approved', is_deleted=False),
                name='idx_product_feed'
            ),
            models.Index(fields=['status']),
        ]
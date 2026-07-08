import uuid
from typing import TYPE_CHECKING

from common.managers import SoftDeleteManager, SoftDeleteQuerySet
from django.db import models

if TYPE_CHECKING:
    from users.models import User

    from .models.products import Product


class ProductQuerySet(SoftDeleteQuerySet):

    def approved(self) -> models.QuerySet["Product"]:
        return self.alive().filter(status=self.model.Status.APPROVED)

    def pending(self) -> models.QuerySet["Product"]:
        return self.alive().filter(status=self.model.Status.PENDING)

    def draft(self) -> models.QuerySet["Product"]:
        return self.alive().filter(status=self.model.Status.DRAFT)

    def archived(self) -> models.QuerySet["Product"]:
        return self.alive().filter(status=self.model.Status.ARCHIVED)

    def for_feed(self) -> models.QuerySet["Product"]:
        return self.approved().order_by("-created_at")

    def for_category(self, category_id: uuid.UUID) -> models.QuerySet["Product"]:
        return self.approved().filter(category_id=category_id)

    def for_owner(self, owner: "User") -> models.QuerySet["Product"]:
        return self.alive().filter(owner=owner).order_by("-created_at")


ProductManager = SoftDeleteManager.from_queryset(ProductQuerySet)

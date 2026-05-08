from typing import TYPE_CHECKING, cast

from django.db import models

if TYPE_CHECKING:
    from users.models import User

    from .models import Product


class ProductQuerySet(models.QuerySet["Product"]):

    def alive(self) -> models.QuerySet["Product"]:
        return self.filter(is_deleted=False)

    def deleted(self) -> models.QuerySet["Product"]:
        return self.filter(is_deleted=True)

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

    def for_category(self, category_id: int) -> models.QuerySet["Product"]:
        return self.approved().filter(category_id=category_id)

    def for_owner(self, owner: "User") -> models.QuerySet["Product"]:
        return self.alive().filter(owner=owner).order_by("-created_at")


class ProductManager(models.Manager["Product"]):

    def get_queryset(self) -> models.QuerySet["Product"]:
        return ProductQuerySet(self.model, using=self._db).alive()

    def for_feed(self) -> models.QuerySet["Product"]:
        qs = cast(ProductQuerySet, self.get_queryset())
        return qs.for_feed()

    def approved(self) -> models.QuerySet["Product"]:
        qs = cast(ProductQuerySet, self.get_queryset())
        return qs.approved()

    def for_category(self, category_id: int) -> models.QuerySet["Product"]:
        qs = cast(ProductQuerySet, self.get_queryset())
        return qs.for_category(category_id)

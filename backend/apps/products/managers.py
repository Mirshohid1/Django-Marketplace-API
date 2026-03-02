from django.db import models


class ProductQuerySet(models.QuerySet):

    def alive(self):
        return self.filter(is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=True)

    def approved(self):
        return self.alive().filter(status=Product.Status.APPROVED)

    def pending(self):
        return self.alive().filter(status=Product.Status.PENDING)

    def draft(self):
        return self.alive().filter(status=Product.Status.DRAFT)

    def archived(self):
        return self.alive().filter(status=Product.Status.ARCHIVED)

    def for_feed(self):
        return self.approved().order_by("-created_at")

    def for_category(self, category_id):
        return self.approved().filter(category_id=category_id)

    def for_owner(self, owner):
        return self.alive().filter(owner=owner).order_by("-created_at")

    def soft_delete(self):
        return self.update(is_deleted=True)

    def restore(self):
        return self.update(is_deleted=False)


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db).alive()

    def for_feed(self):
        return self.get_queryset().for_feed()

    def approved(self):
        return self.get_queryset().approved()

    def for_category(self, category_id):
        return self.get_queryset().for_category(category_id)

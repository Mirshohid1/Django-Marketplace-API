from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def soft_delete(self):
        return super().update(
            is_deleted=True,
            deleted_at=timezone.now(),
        )

    def alive(self):
        return self.filter(is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=True)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(
            self.model,
            using=self._db,
        ).alive()

from rest_framework import serializers

from ..models.catalogs import Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "id",
            "slug",
            "name",
            "created_at",
            "updated_at",
            "deleted_at",
        )

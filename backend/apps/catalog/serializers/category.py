from rest_framework import serializers

from ..models.catalogs import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "slug",
            "parent",
            "name",
            "is_active",
            "created_at",
            "updated_at",
            "deleted_at",
        )

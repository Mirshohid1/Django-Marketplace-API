from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializer.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    parent_id = serializers.IntegerField(read_only=True)
    parent_name = serializers.CharField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'created_at', 'updated_at', 'parent_id', 'parent_name')


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'parent_id')

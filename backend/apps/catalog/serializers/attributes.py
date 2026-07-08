from rest_framework import serializers

from ..models.attributes import Attribute, AttributeValue, VariantAttributeValue


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = (
            "id",
            "slug",
            "name",
            "type",
            "is_variant_only",
            "created_at",
            "updated_at",
            "deleted_at",
        )


class AttributeValueOutputSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer()

    class Meta:
        model = AttributeValue
        fields = (
            "id",
            "attribute",
            "value",
            "created_at",
            "updated_at",
            "deleted_at",
        )


class VariantAttributeValueOutputSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer()
    value = AttributeValueOutputSerializer()

    class Meta:
        model = VariantAttributeValue
        fields = (
            "id",
            "attribute",
            "value",
            "created_at",
            "updated_at",
            "deleted_at",
        )


class AttributeValueInputSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)

    attribute = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all())

    value = serializers.CharField()


class VariantAttributeValueInputSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)

    attribute = serializers.PrimaryKeyRelatedField(queryset=Attribute.objects.all())

    value = serializers.PrimaryKeyRelatedField(queryset=AttributeValue.objects.all())

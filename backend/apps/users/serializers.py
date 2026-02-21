from rest_framework import serializers
from django.db import transaction
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'username', 'email', 'password'
        )

    def validate_password(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('Passwords must match')

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('Email already registered')
        elif User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError('Username already registered')

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop('password_confirm')

        user = User.objects.create(**validated_data)
        return user


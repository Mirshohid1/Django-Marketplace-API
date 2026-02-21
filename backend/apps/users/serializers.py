from rest_framework import serializers
from django.db import transaction
from django.core.exceptions import ValidationError as DjangoValidationError
from .service.validators import PasswordValidationService
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'username', 'email',
            'password', 'password_confirm',
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password': 'Passwords must match'})

        user_attrs = {
            'username': attrs.get('username'),
            'email': attrs.get('email'),
            'first_name': attrs.get('first_name'),
            'last_name': attrs.get('last_name'),
        }

        try:
            PasswordValidationService.validate(attrs['password'], **user_attrs)
        except DjangoValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        if User.objects.filter(email=user_attrs['email']).exists():
            raise serializers.ValidationError('Email already registered')

        if user_attrs['username'] and User.objects.filter(username=user_attrs['username']).exists():
            raise serializers.ValidationError('Username already registered')

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop('password_confirm')

        user = User.objects.create_user(**validated_data)
        return user


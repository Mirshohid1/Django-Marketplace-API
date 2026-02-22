from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import Q
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


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')

        user = User.objects.filter(Q(email=login) | Q(username=login)).first()
        if not user:
            raise serializers.ValidationError("There is no user with this username or email.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password.")

        refresh = RefreshToken.for_user(user)
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'username', 'email',
        )


class UserOutPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name', 'last_name',
            'username', 'email',
            'is_active', 'is_staff',
        )
        read_only_fields = fields
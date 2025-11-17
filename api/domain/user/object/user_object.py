from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import BaseUserManager
from api.domain.user.models.user import User

class UserObject(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    email = serializers.EmailField(
        max_length=64,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = [
            "id",
            "role",
            "email",
            "password",
            "email_verified_at",
            "remember_token",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at"
        ]

    def validate_email(self, value):
        # standardized email normalization used by Django
        return BaseUserManager.normalize_email(value)

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        if password:
            validated_data["password"] = make_password(password)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # handle password explicitly so empty values don't overwrite
        password = validated_data.pop("password", None)
        if password:
            instance.password = make_password(password)
        # update other fields
        return super().update(instance, validated_data)

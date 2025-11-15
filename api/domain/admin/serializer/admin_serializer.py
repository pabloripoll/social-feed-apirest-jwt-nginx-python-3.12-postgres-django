from rest_framework import serializers
from .models import Admin, AdminProfile, AdminAccessLog

class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = ["id", "user", "nickname", "avatar", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

class AdminSerializer(serializers.ModelSerializer):
    profile = AdminProfileSerializer(source="user.admin_profile", read_only=True)

    class Meta:
        model = Admin
        fields = ["id", "user", "region", "is_active", "is_banned", "created_at", "updated_at", "profile"]
        read_only_fields = ["id", "created_at", "updated_at"]

class AdminAccessLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAccessLog
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

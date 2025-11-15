from django.utils import timezone
from rest_framework import serializers

from api.domain.user.model.user import User
from api.domain.user.model.member_access_log import MemberAccessLog


class MemberAccessLogSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    refresh_count = serializers.IntegerField(read_only=True)
    requests_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = MemberAccessLog
        fields = [
            "id",
            "user_id",
            "is_terminated",
            "is_expired",
            "expires_at",
            "refresh_count",
            "created_at",
            "updated_at",
            "ip_address",
            "user_agent",
            "requests_count",
            "payload",
            "token",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "refresh_count",
            "requests_count"
        ]

    def validate_expires_at(self, value):
        """
        Ensure expires_at is in the future (relative to now).
        """
        now = timezone.now()
        if value <= now:
            raise serializers.ValidationError("expires_at must be a future datetime.")
        return value

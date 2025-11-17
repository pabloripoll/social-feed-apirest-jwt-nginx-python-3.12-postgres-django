from rest_framework import serializers
from api.domain.member.models.member_notification import MemberNotification

class MemberNotificationObject(serializers.ModelSerializer):
    class Meta:
        model = MemberNotification
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at"
        ]

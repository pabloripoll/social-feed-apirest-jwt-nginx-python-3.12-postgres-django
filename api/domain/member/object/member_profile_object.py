from rest_framework import serializers
from api.domain.member.model.member_profile import MemberProfile

class MemberProfileObject(serializers.ModelSerializer):
    class Meta:
        model = MemberProfile
        fields = [
            "id",
            "user_id",
            "nickname",
            "avatar",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at"
        ]

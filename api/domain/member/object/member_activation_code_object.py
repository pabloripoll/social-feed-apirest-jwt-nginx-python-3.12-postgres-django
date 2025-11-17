from rest_framework import serializers
from api.domain.member.models.member_activation_code import MemberActivationCode

class MemberActivationCodeObject(serializers.ModelSerializer):
    class Meta:
        model = MemberActivationCode
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at"
        ]

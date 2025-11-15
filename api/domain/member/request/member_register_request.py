from rest_framework import serializers

class MemberRegisterRequest(serializers.Serializer):
    email = serializers.EmailField(max_length=64)
    password = serializers.CharField(min_length=8, write_only=True)
    nickname = serializers.CharField(max_length=32)
    region_id = serializers.IntegerField(required=False, allow_null=True)

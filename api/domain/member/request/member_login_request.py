from rest_framework import serializers

class MemberLoginRequest(serializers.Serializer):
    email = serializers.EmailField(max_length=64)
    password = serializers.CharField(min_length=8, write_only=True)

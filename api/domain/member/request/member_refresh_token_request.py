from rest_framework import serializers

class MemberRefreshTokenRequest(serializers.Serializer):
    refresh = serializers.CharField()
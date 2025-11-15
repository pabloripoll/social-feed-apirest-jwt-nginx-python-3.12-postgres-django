from rest_framework import serializers

class MemberLogoutRequest(serializers.Serializer):
    refresh = serializers.CharField()

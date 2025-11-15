from rest_framework import serializers

class MemberActivationCodeRequest(serializers.Serializer):
    email = serializers.EmailField(max_length=64)
    code = serializers.CharField(max_length=64)

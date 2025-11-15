from rest_framework import serializers
from .models import Post, PostCategory, PostVisit, PostVote, PostReport, PostReportType

class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

class PostVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVote
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

class PostReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReport
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]

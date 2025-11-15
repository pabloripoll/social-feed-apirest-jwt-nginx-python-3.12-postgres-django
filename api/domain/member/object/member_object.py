from rest_framework import serializers
from api.domain.member.model.member import Member
from api.domain.member.object.member_profile_object import MemberProfileObject

class MemberObject(serializers.ModelSerializer):
    profile = MemberProfileObject(source="user.member_profile", read_only=True)

    class Meta:
        model = Member
        fields = [
            "id",
            "uid",
            "user_id",
            "region_id",
            "is_active",
            "is_banned",
            "following_count",
            "followers_count",
            "posts_count",
            "posts_votes_up_count",
            "posts_votes_down_count",
            "created_at",
            "updated_at",
            "profile"
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at"
        ]

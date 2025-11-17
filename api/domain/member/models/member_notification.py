from django.db import models
from api.domain.user.models.user import User
from .member_notification_type import MemberNotificationType  # adjust this import to match your file layout


class MemberNotification(models.Model):
    id = models.BigAutoField(primary_key=True)
    notification_type_id = models.ForeignKey(
        MemberNotificationType,
        on_delete=models.CASCADE,
        db_column="notification_type_id",
        related_name="notifications",
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="notifications",
    )
    is_opened = models.BooleanField(default=False)
    opened_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=512)
    last_member_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column="last_member_user_id",
        related_name="notifications_last_member",
    )
    last_member_nickname = models.CharField(max_length=32, null=True, blank=True)
    last_member_avatar = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "members_notifications"
        indexes = [
            models.Index(fields=["opened_at"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Notification({self.id}) for user {self.user_id}"

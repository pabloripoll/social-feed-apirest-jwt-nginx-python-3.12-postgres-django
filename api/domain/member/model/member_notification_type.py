from django.db import models

class MemberNotificationType(models.Model):
    id = models.BigAutoField(primary_key=True)
    key = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=64)
    message_singular = models.CharField(max_length=512, null=True, blank=True)
    message_multiple = models.CharField(max_length=512, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "members_notification_types"

    def __str__(self):
        return f"{self.key} - {self.title}"
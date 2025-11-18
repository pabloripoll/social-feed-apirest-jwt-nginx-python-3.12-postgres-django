from django.db import models
from api.domain.user.models.user import User

class UserPasswordResetToken(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="reset_tokens"   # reverse: user.reset_tokens.all()
    )
    email = models.EmailField(max_length=64, primary_key=True)
    token = models.TextField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_password_reset_tokens"
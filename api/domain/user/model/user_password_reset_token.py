from django.db import models

class PasswordResetToken(models.Model):
    email = models.EmailField(max_length=64, primary_key=True)
    token = models.TextField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "password_reset_tokens"
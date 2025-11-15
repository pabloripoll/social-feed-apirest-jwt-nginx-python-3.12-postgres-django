from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Minimal models: using Django's built-in User. Add profile fields if needed.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Profile({self.user.username})"

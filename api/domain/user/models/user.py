from django.db import models

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    role = models.CharField(max_length=16)
    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    remember_token = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]

    def __str__(self):
        return self.email

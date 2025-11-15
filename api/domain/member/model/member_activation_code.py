from __future__ import annotations
from typing import Optional

from django.db import models, transaction, IntegrityError
from django.conf import settings
from api.domain.user.model.user import User
import secrets


class MemberActivationCode(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=32, unique=True)
    user_id = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="activation_codes"
    )
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "members_activation_codes"

    def __str__(self):
        return f"ActivationCode(code={self.code}, user_id={self.user_id})"

    @staticmethod
    def _generate_code() -> str:
        """Generate a 32-character hex code."""
        return secrets.token_hex(16)

    @classmethod
    def create_for_user(cls, user: User, is_active: Optional[bool] = None, max_tries: int = 6) -> "MemberActivationCode":
        """
        Create and return a MemberActivationCode for the given user.
        Ensures the 'code' is unique by retrying on IntegrityError.
        Raises RuntimeError if unable to create after max_tries.
        """
        if is_active is None:
            requires_activation = bool(getattr(settings, "LOGIN_ACTIVATION_CODE", False))
            is_active = not requires_activation

        for attempt in range(max_tries):
            code = cls._generate_code()
            try:
                with transaction.atomic():
                    return cls.objects.create(user=user, code=code, is_active=is_active)
            except IntegrityError:
                # collision on unique code; retry
                if attempt == max_tries - 1:
                    raise
                continue

        # If we somehow exit the loop without creating or raising, make failure explicit
        raise RuntimeError("Failed to generate unique activation code after retries.")

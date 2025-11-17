from django.db import models, transaction, IntegrityError
from api.domain.user.models.user import User
from api.domain.geo.models.geo_region import GeoRegion
import time
import secrets

class Member(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.BigIntegerField(unique=True)
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="members"   # reverse: user.members.all()
    )
    region_id = models.ForeignKey(
        GeoRegion,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        db_column="region_id",
        related_name="members"    # reverse: region.members_in_region.all()
    )
    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)
    following_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    posts_votes_up_count = models.IntegerField(default=0)
    posts_votes_down_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "members"
        indexes = [
            models.Index(fields=["uid"]),
        ]

    def __str__(self):
        return f"Member(uid={self.uid}, user_id={self.user_id})"

    @classmethod
    def generate_uid(cls) -> int:
        """
        Generate a numeric uid. Uses high-resolution time plus random bits to reduce collisions.
        Adjust algorithm if you need monotonic ids or different size.
        """
        # time_ns on its own might collide under heavy concurrency; mix with a few random bits
        ts = time.time_ns() % (2**52)             # keep it within a comfortable range
        rand = secrets.randbits(11)               # add 11 bits of randomness -> very low collision risk
        return (ts << 11) | rand

    def save(self, *args, **kwargs):
        """
        On create, ensure a unique uid is assigned. Use a retry loop and catch IntegrityError to handle
        concurrent inserts that generate the same uid.
        """
        if not self.uid:
            # only generate when uid is not set
            max_tries = 6
            for attempt in range(max_tries):
                self.uid = self.generate_uid()
                try:
                    # try to save; if unique collision occurs, IntegrityError will be raised and we retry
                    with transaction.atomic():
                        super().save(*args, **kwargs)
                    return
                except IntegrityError:
                    # possible uid collision - retry
                    if attempt == max_tries - 1:
                        raise
                    # on retry, loop continues and new uid will be generated
                    continue
        else:
            # uid is already set -> normal save (update)
            super().save(*args, **kwargs)
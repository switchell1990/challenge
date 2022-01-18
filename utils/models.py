from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(
        verbose_name=_("Creation date"), auto_now_add=True, null=True, db_index=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated date"), auto_now_add=True, null=True, db_index=True
    )

    class Meta:
        abstract = True

import uuid
from typing import Dict

from django.db import models
from django.db.models.base import ModelBase
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from utils.constants import ALLOW_NOT_NULL, CHAR_NOT_NULL_BLANK, NULL_BLANK
from utils.models import BaseModel


class GendorChoice(models.TextChoices):
    MALE = "MALE", _("Male")
    FEMALE = "FEMALE", _("Female")


class TitleChoice(models.TextChoices):
    MR = "MR", _("Mr")
    MRS = "MRS", _("Mrs")
    MISS = "MISS", _("Miss")
    MS = "MS", _("Ms")


class School(BaseModel):
    name = models.CharField(max_length=20, db_index=True, unique=True, **ALLOW_NOT_NULL)
    code = models.CharField(max_length=20, **ALLOW_NOT_NULL)
    location = models.CharField(db_index=True, **CHAR_NOT_NULL_BLANK)
    student_max_number = models.PositiveIntegerField(default=100)

    class Meta:
        db_table: str = "school"

    def __str__(self) -> str:
        return str(self.name)


@receiver(post_save, sender=School)
def set_null_inactive(sender: ModelBase, instance: School, **kwargs: Dict) -> None:
    # If school is set to null, then set all related items to None so the students can be reassigned to another school.
    if not instance.is_active:
        instance.student.all().update(school_id=None)


class Student(BaseModel):
    title = models.CharField(max_length=4, choices=TitleChoice.choices)
    first_name = models.CharField(max_length=20, **ALLOW_NOT_NULL)
    last_name = models.CharField(max_length=20, **ALLOW_NOT_NULL)
    age = models.PositiveIntegerField()
    gender = models.CharField(
        choices=GendorChoice.choices, max_length=6, **ALLOW_NOT_NULL
    )
    identification = models.UUIDField(default=uuid.uuid4, unique=True)
    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        related_name="student",
        **NULL_BLANK,
    )

    class Meta:
        db_table: str = "student"

    def __str__(self) -> str:
        return f"{self.first_name} - {self.last_name}"

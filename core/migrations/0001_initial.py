# Generated by Django 3.2 on 2022-01-17 14:50

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="School",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        null=True,
                        verbose_name="Creation date",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        null=True,
                        verbose_name="Updated date",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=20, unique=True)),
                ("code", models.CharField(max_length=20)),
                ("location", models.CharField(db_index=True, max_length=100)),
                ("student_max_number", models.PositiveIntegerField(default=100)),
            ],
            options={
                "db_table": "school",
            },
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        null=True,
                        verbose_name="Creation date",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_index=True,
                        null=True,
                        verbose_name="Updated date",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        choices=[
                            ("MR", "Mr"),
                            ("MRS", "Mrs"),
                            ("MISS", "Miss"),
                            ("MS", "Ms"),
                        ],
                        max_length=4,
                    ),
                ),
                ("first_name", models.CharField(max_length=20)),
                ("last_name", models.CharField(max_length=20)),
                ("age", models.PositiveIntegerField()),
                (
                    "gender",
                    models.CharField(
                        choices=[("MALE", "Male"), ("FEMALE", "Female")], max_length=6
                    ),
                ),
                ("identification", models.UUIDField(default=uuid.uuid4, unique=True)),
                (
                    "school",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="student",
                        to="core.school",
                    ),
                ),
            ],
            options={
                "db_table": "student",
            },
        ),
    ]
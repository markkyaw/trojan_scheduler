# Generated by Django 4.0 on 2022-03-20 19:40

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BasicClassInfo",
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
                (
                    "class_code",
                    models.CharField(default=None, max_length=100, null=True),
                ),
                (
                    "class_number",
                    models.CharField(default=None, max_length=200, null=True),
                ),
                ("year", models.IntegerField()),
                (
                    "semester",
                    models.IntegerField(
                        choices=[(1, "Spring"), (2, "Summer"), (3, "Fall")]
                    ),
                ),
                (
                    "min_units",
                    models.DecimalField(
                        decimal_places=1,
                        default=0.0,
                        max_digits=3,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(12),
                        ],
                    ),
                ),
                (
                    "max_units",
                    models.DecimalField(
                        decimal_places=1,
                        default=0,
                        max_digits=3,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(12),
                        ],
                    ),
                ),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Instructor",
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
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="BasicClassSection",
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
                ("section", models.CharField(max_length=50)),
                ("session", models.CharField(max_length=3)),
                (
                    "section_type",
                    models.IntegerField(
                        choices=[
                            (1, "Lecture"),
                            (2, "Discussion"),
                            (3, "Lab"),
                            (4, "Quiz"),
                        ]
                    ),
                ),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                ("days", models.CharField(default="0000000", max_length=7)),
                ("location_building", models.CharField(max_length=50)),
                (
                    "location_room",
                    models.CharField(default=None, max_length=50, null=True),
                ),
                (
                    "class_info",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="class_section",
                        to="classes.basicclassinfo",
                    ),
                ),
                (
                    "instructor",
                    models.ManyToManyField(
                        related_name="classes", to="classes.Instructor"
                    ),
                ),
            ],
        ),
    ]

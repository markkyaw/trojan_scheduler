from curses.ascii import NUL

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class ClassSemester(models.IntegerChoices):
    SPRING = 1, _("Spring")
    SUMMER = 2, _("Summer")
    FALL = 3, _("Fall")


class SectionType(models.IntegerChoices):
    LECTURE = 1, _("Lecture")
    DISCUSSION = 2, _("Discussion")
    LAB = 3, _("Lab")
    QUIZ = 4, _("Quiz")


# Create your models here.
class Instructor(models.Model):
    name = models.CharField(
        max_length=200,
    )


class BasicClassInfo(models.Model):
    """
    class_code: CSCI
    class_section: 102L
    year: 2022
    semester: 1
    min_units: 2
    max_units: 2
    description: Fundamental concepts of algorithmic thinking as a primer to programming. Introduction to C++.
    """

    class_code = models.CharField(max_length=100, default=None, null=True)
    class_section = models.CharField(max_length=200, default=None, null=True)
    year = models.IntegerField()
    semester = models.IntegerField(choices=ClassSemester.choices)
    min_units = models.DecimalField(
        decimal_places=1,
        max_digits=3,
        default=0.0,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
    )
    max_units = models.DecimalField(
        decimal_places=1,
        max_digits=3,
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
    )
    description = models.TextField()


class BasicClassSection(BasicClassInfo):
    """
    The model will need to store
    - Section - from parent
    - Session - done
    - Type - done
    - Time
        - Start time
        - End time
    - Days - done
    - Instructor - done
    - Location
        - Building
        - Room #

    Notes:
    - Maybe implement default values for future semesters when not all values have been assigned.
    """

    session = models.CharField(
        max_length=3,
    )
    type = models.IntegerField(choices=SectionType.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = models.CharField(
        max_length=7,
        default="0000000",
    )
    instructor = models.ManyToManyField(Instructor)
    location_building = models.CharField(
        max_length=50,
    )
    location_room = models.CharField(
        max_length=50,
        default=None,
        null=True,
    )

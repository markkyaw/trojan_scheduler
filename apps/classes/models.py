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
    LECTURE_LAB = 5, _("Lecture-Lab")


# Create your models here.
class Instructor(models.Model):
    name = models.CharField(
        max_length=200,
    )


class BasicClassInfo(models.Model):
    """
    class_code: CSCI
    class_number: 102L
    year: 2022
    semester: 1
    min_units: 2
    max_units: 2
    description: Fundamental concepts of algorithmic thinking as a primer to programming. Introduction to C++.
    """

    class_code = models.CharField(max_length=100, default=None, null=True)
    class_number = models.CharField(max_length=200, default=None, null=True)
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


class BasicClassSection(models.Model):
    """
    Sample Info.
    - Class Info: Foreign key to basic class info object CSCI 270.
    - Section: 41635R
    - Session: 001
    - Type: 1 (Lecture)
    - Time
        - Start time: 1230PM
        - End time: 150PM
    - Days: 1010000 (Translates to: MW)
    - Instructor: David Kempe
    - Location
        - Building: ONLINE
        - Room #: NULL

    Notes:
    - Maybe implement default values for future semesters when not all values have been assigned.
    """

    class_info = models.ForeignKey(
        BasicClassInfo, related_name="class_section", on_delete=models.CASCADE
    )
    section = models.CharField(
        max_length=50,
    )
    session = models.CharField(
        max_length=3,
    )
    section_type = models.IntegerField(choices=SectionType.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = models.CharField(
        max_length=7,
        default="0000000",
    )
    instructor = models.ManyToManyField(Instructor, related_name="classes")
    location_building = models.CharField(
        max_length=50,
    )
    location_room = models.CharField(
        max_length=50,
        default=None,
        null=True,
    )

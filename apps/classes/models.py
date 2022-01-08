from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class ClassSemester(models.IntegerChoices):
    SPRING = 1, _("Spring")
    SUMMER = 2, _("Summer")
    FALL = 3, _("Fall")


# Create your models here.
class BasicClassInfo(models.Model):
    class_code = models.CharField(max_length=100, default=None, null=True)
    class_section = models.CharField(max_length=200, default=None, null=True)
    year = models.IntegerField()
    semester = models.IntegerField(choices=ClassSemester.choices)
    min_units = models.IntegerField(
        default=0, validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    max_units = models.IntegerField(
        default=0, validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    description = models.TextField()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import models

from apps.classes.models import BasicClassSection

from ..classes import *


# Create your models here.
class UserInfo(models.Model):
    """
    Inherits from the User class model, allowing authentication with the server.
    """

    user = models.OneToOneField(User, related_name="info", on_delete=models.CASCADE)
    classes = models.ManyToManyField(BasicClassSection, related_name="user_classes")

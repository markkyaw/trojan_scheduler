from django.urls import re_path

from .views import *

urlpatterns = [
	re_path(r"^get_first/?$", BasicClassInfoView.as_view(), name="get_first"),
]
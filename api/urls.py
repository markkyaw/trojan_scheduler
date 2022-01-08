from django.contrib import admin
from django.urls import include, re_path

admin.autodiscover()

urlpatterns = [
		re_path(r"^v1/", include(("api.v1.urls", "v1"), namespace="v1"))
]


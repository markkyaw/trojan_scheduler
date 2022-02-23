from django.urls import include, re_path

urlpatterns = [
    re_path(
        r"^classes/",
        include(("api.v1.classes.urls", "classes"), namespace="classes"),
        name="classes",
    )
]

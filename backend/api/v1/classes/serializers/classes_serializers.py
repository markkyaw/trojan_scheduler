from apps.classes.models import BasicClassInfo
from rest_framework import serializers


class BasicClassInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicClassInfo
        fields = "__all__"

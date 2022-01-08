from rest_framework import serializers

from apps.classes.models import BasicClassInfo


class BasicClassInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicClassInfo
        fields = "__all__"

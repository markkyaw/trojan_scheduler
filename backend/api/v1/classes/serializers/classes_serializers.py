from apps.classes.models import BasicClassInfo, BasicClassSection
from rest_framework import serializers


class BasicClassInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicClassInfo
        fields = "__all__"


class BasicClassSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicClassSection
        fields = "__all__"


class GetSectionsSerializer(serializers.Serializer):
    class_code = serializers.CharField(required=True)
    class_number = serializers.CharField(required=True)

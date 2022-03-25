import json

from api.v1.classes.serializers import *
from apps.classes.models import BasicClassInfo, BasicClassSection
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


class BasicClassInfoView(GenericAPIView):
    serializer_class = BasicClassInfoSerializer

    def get(self, request, format=None):
        return_status = status.HTTP_200_OK
        ret = BasicClassInfoSerializer(BasicClassInfo.objects.get(id=1)).data

        return Response(ret, return_status)


class GetSectionsView(GenericAPIView):
    serializer_class = GetSectionsSerializer

    def get(self, request):
        serializer = GetSectionsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"invalid request"}, status.HTTP_400_BAD_REQUEST)
        ret = dict()
        ret["data"] = []
        input = serializer.validated_data
        bcs = BasicClassInfo.objects.get(
            class_code=input.get("class_code"), class_number=input.get("class_number")
        ).class_section.all()
        for section in bcs:
            ret["data"].append(BasicClassSectionSerializer(section).data)

        return Response(ret, status.HTTP_200_OK)

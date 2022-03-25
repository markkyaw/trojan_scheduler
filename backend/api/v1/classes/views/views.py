import json

from api.v1.classes.serializers import *
from apps.classes.models import BasicClassInfo
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

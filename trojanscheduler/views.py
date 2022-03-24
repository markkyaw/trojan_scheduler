# stolen from github
import json

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.classes.serializers import *
from apps.classes.models import BasicClassInfo


class BasicClassInfoView(GenericAPIView):
    serializer_class = BasicClassInfoSerializer

    def get(self, request, format=None):
        return_status = status.HTTP_200_OK
        ret = BasicClassInfoSerializer(BasicClassInfo.objects.get(id=1)).data

        return Response(ret, return_status)

    # Create a view that will return a list of basicclasssection objects based on class_code and class_section
    # Ex: If the query passes in "CSCI 102" expect to see all sections that contains CSCI 102
    #    If the query passes in "all" return all classes in basicclassinfo objects ordered alphabetically

    def class_section_search(query):
        if query == "all":
            return BasicClassInfo.objects.order_by("class_code")

        code = query[: query.index(" ")]
        section = query[query.index(" ") + 1 :]

        return BasicClassInfo.objects.filter(class_code=code, class_section=section)

    # Create another view that returns a list of basicclassinfo objects based on class code
    # If the query passes in is "CSCI" expect to see all basicclassinfo that contains "CSCI" so it'll have CSCI 102, CSCI 103, ...

    def class_code_search(code):
        return BasicClassInfo.objects.filter(class_code=code)

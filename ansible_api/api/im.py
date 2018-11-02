# -*- coding: utf-8 -*-
#

"""
Immediately run adhoc and playbook
"""

from rest_framework import permissions, generics
from rest_framework.response import Response

from ..serializers import IMPlaybookSerializer, IMAdHocSerializer
from ..tasks import execute_playbook, execute_adhoc

__all__ = ['IMPlaybookApi', 'IMAdHocApi']


class IMPlaybookApi(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = IMPlaybookSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            playbook = serializer.save()
            task = execute_playbook.delay(playbook.id, save_history=False)
            return Response({'task': task.id})
        else:
            return Response({"error": serializer.errors})


class IMAdHocApi(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = IMAdHocSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            adhoc = serializer.save()
            task = execute_adhoc.delay(adhoc.id, save_history=False)
            return Response({'task': task.id})
        else:
            return Response({"error": serializer.errors})

from typing import Dict, Tuple, Union

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import School, Student


class BaseModel(ModelViewSet):
    permission_classes: Tuple = (AllowAny,)

    def destroy(self, request: Request, *args: Tuple, **kwargs: Dict) -> Response:
        instance: Union[School, Student] = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

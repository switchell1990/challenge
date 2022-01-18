from typing import Dict, Tuple, Type

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.filters import SchoolFilter, StudentFilter, StudentNestedFilter
from core.models import School, Student
from core.serializers import (
    SchoolSerializer,
    StudentNestedSerializer,
    StudentSerializer,
)
from utils.pagination import LargeSizePagination, StandardSizePagination


class BaseSerializer(ModelViewSet):
    permission_classes: Tuple = (AllowAny,)

    def destroy(self, request: Request, *args: Tuple, **kwargs: Dict) -> Response:
        instance: School = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SchoolViewSet(BaseSerializer):
    """
    list:
    Return a list of active existing schools.

    create:
    Create a new instance of a school.

    retrieve:
    Retrieve a school instance by ID.

    update:
    Update a school instance record.

    partial_update:
    Update selected fields, e.g. name, location.

    delete:
    Delete an instance of a school.
    """
    queryset: School = School.objects.filter(is_active=True).order_by("-created_at")
    serializer_class: Type[SchoolSerializer] = SchoolSerializer
    filterset_class: Type[SchoolFilter] = SchoolFilter
    pagination_class: Type[StandardSizePagination] = StandardSizePagination


class StudentViewSet(BaseSerializer):
    """
    list:
    Return a list of active existing students.

    create:
    Create a new instance of a student.

    retrieve:
    Retrieve a student instance by ID.

    update:
    Update a student instance record.

    partial_update:
    Update selected fields, e.g. name, location.

    delete:
    Delete an instance of a student
    """
    queryset: Student = Student.objects.filter(is_active=True).order_by("-created_at")
    serializer_class: Type[StudentSerializer] = StudentSerializer
    filterset_class: Type[StudentFilter] = StudentFilter
    pagination_class: Type[LargeSizePagination] = LargeSizePagination


class StudentNestedViewSet(BaseSerializer):
    """
    list:
    Return a list of active existing schools with active students.

    create:
    Create a new instance of a student in a selected school.

    retrieve:
    Retrieve an instance by school and student ID.

    update:
    Update a student instance record.

    partial_update:
    Update selected fields, e.g. name, location.

    delete:
    Delete an instance of a student
    """
    queryset: Student = Student.objects.filter(is_active=True).order_by("-created_at")
    serializer_class: Type[StudentNestedSerializer] = StudentNestedSerializer
    filterset_class: Type[StudentNestedFilter] = StudentNestedFilter
    pagination_class: Type[LargeSizePagination] = LargeSizePagination

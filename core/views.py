from typing import Type

from core.filters import SchoolFilter, StudentFilter, StudentNestedFilter
from core.models import School, Student
from core.serializers import (
    SchoolSerializer,
    StudentNestedSerializer,
    StudentSerializer,
)
from utils.pagination import LargeSizePagination, StandardSizePagination
from utils.views import BaseModel


class SchoolViewSet(BaseModel):
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


class StudentViewSet(BaseModel):
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


class StudentNestedViewSet(BaseModel):
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

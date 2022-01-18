from typing import Tuple, Type

import django_filters

from core.models import School, Student


class SchoolFilter(django_filters.FilterSet):
    class Meta:
        model: Type[School] = School
        fields: Tuple = (
            "name",
            "location",
        )


class StudentFilter(django_filters.FilterSet):
    school: django_filters.CharFilter = django_filters.CharFilter(
        field_name="school__name", label="school"
    )

    class Meta:
        model: Type[Student] = Student
        fields: Tuple = (
            "first_name",
            "last_name",
            "school",
        )


class StudentNestedFilter(django_filters.FilterSet):
    class Meta:
        model: Type[Student] = Student
        fields: Tuple = ("first_name", "last_name")

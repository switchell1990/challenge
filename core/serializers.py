from typing import Dict, Tuple, Type, Union

from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    ValidationError,
)

from core.models import School, Student
from services.core_services import age_validation_check, is_max_student_count


class SchoolSerializer(ModelSerializer):
    class Meta:
        model: Type[School] = School
        fields: str = "__all__"
        read_only_fields: Tuple = ("is_active", "created_at", "updated_at")


class StudentSerializer(ModelSerializer):
    school_details: SchoolSerializer = SchoolSerializer(source="school", read_only=True)
    # Added in so we able to pass School_ID instead of School Name
    school: PrimaryKeyRelatedField = PrimaryKeyRelatedField(
        queryset=School.objects.all(), write_only=True
    )

    class Meta:
        model: Type[Student] = Student
        fields: str = "__all__"
        read_only_fields: Tuple = (
            "is_active",
            "identification",
        )

    def create(self, validated_data: Dict) -> Union[Student, ValidationError]:
        if age_validation_check(validated_data["age"]):
            raise ValidationError(
                "Students need to be age between 10 to 20 to register!"
            )

        if is_max_student_count(validated_data["school"]):
            raise ValidationError("Unable to add student to school as it is full!")

        return super().create(validated_data)

    def update(
        self, instance: Student, validated_data: Dict
    ) -> Union[School, ValidationError]:
        school: School = validated_data.get("school", None)

        if school and is_max_student_count(school):
            raise ValidationError("Unable to add student to school as it is full!")

        return super().update(instance, validated_data)


class StudentNestedSerializer(ModelSerializer):
    school_details: SchoolSerializer = SchoolSerializer(source="school", read_only=True)

    class Meta:
        model: Type[Student] = Student
        fields: str = "__all__"
        read_only_fields: Tuple = ("is_active", "identification", "school")

    def create(self, validated_data: Dict) -> Union[School, ValidationError]:
        school_object: School = School.objects.get(
            pk=self.context["view"].kwargs["school_pk"]
        )
        validated_data["school"] = school_object

        if age_validation_check(validated_data["age"]):
            raise ValidationError(
                "Students need to be age between 10 to 20 to register!"
            )

        return super().create(validated_data)

import pytest

from core.models import School, Student


@pytest.mark.django_db
def test_school_model_str() -> None:
    school: School = School.objects.get(pk=1)

    assert str(school) == school.name


@pytest.mark.django_db
def test_student_model_str() -> None:
    student: Student = Student.objects.get(pk=1)

    assert str(student) == f"{student.first_name} - {student.last_name}"

import pytest
from django.core.management import call_command
from django.urls import reverse
from pytest import fixture
from pytest_django.plugin import _DatabaseBlocker
from rest_framework.test import APIClient

from core.models import School, Student

SCHOOL_LIST_URL: str = reverse("api:schools-list")
SCHOOL_DETAIL_URL: str = "api:schools-detail"
SCHOOL_STUDENT_LIST_URL: str = "api:school-students-list"
SCHOOL_STUDENT_DETAIL_URL: str = "api:school-students-detail"
STUDENT_LIST_URL: str = reverse("api:students-list")
STUDENT_DETAIL_URL: str = "api:students-detail"
SCHOOL_FULL_ERROR_MESSAGE: str = "Unable to add student to school as it is full!"


@fixture()
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup: None, django_db_blocker: _DatabaseBlocker) -> None:
    with django_db_blocker.unblock():
        call_command("createdata")


@pytest.mark.django_db
@fixture()
def get_school_name_data() -> str:
    return str(School.objects.values("name")[0]["name"])


@fixture()
def get_school_location_data() -> str:
    return str(School.objects.values("location")[0]["location"])


@fixture()
def get_student_first_name_data() -> str:
    return str(Student.objects.values("first_name")[0]["first_name"])


@fixture()
def get_student_last_name_data() -> str:
    return str(Student.objects.values("last_name")[0]["last_name"])


@fixture()
def get_id_for_full_school(api_client: APIClient) -> int:
    school: School = School.objects.create(
        name="School America", student_max_number=1, location="Bangkok", code="A10322"
    )
    Student.objects.create(
        title="MR",
        first_name="Heather",
        last_name="Smith",
        age=15,
        gender="FEMALE",
        school=school,
    )
    return int(school.id)

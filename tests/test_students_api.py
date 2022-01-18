from typing import Dict, OrderedDict

import pytest
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
from rest_framework.response import Response
from rest_framework.test import APIClient

from core.models import Student
from tests.conftest import (
    SCHOOL_FULL_ERROR_MESSAGE,
    STUDENT_DETAIL_URL,
    STUDENT_LIST_URL,
)


@pytest.mark.django_db
def test_get_student_list_successful(api_client: APIClient) -> None:

    resp = api_client.get(STUDENT_LIST_URL)

    assert 200 == resp.status_code
    assert isinstance(resp.data, OrderedDict)
    assert 5 == len(resp.json()["results"])


@pytest.mark.django_db
@pytest.mark.parametrize(
    "param_name,search_term",
    [
        ("first_name", lazy_fixture("get_student_first_name_data")),
        ("last_name", lazy_fixture("get_student_last_name_data")),
        ("school", lazy_fixture("get_school_name_data")),
    ],
    ids=[
        "list-student-filter-first_name",
        "list-student-filter-last_name",
        "list-student-filter-school",
    ],
)
def test_student_list_with_filter(
    param_name: str, search_term: str, api_client: APIClient
) -> None:

    url: str = f"{STUDENT_LIST_URL}?{param_name}={search_term}"
    resp: Response = api_client.get(url)

    assert 200 == resp.status_code
    assert (
        search_term == resp.json()["results"][0][param_name]
        if param_name != "school"
        else resp.json()["results"][0]["school_details"]["name"]
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "student_id",
    [(1), (2), (3)],
    ids=[
        "get-student-1-successful",
        "get-student-2-successful",
        "get-student-3-successful",
    ],
)
def test_get_student_by_id_successful(student_id: int, api_client: APIClient) -> None:

    url: str = reverse(STUDENT_DETAIL_URL, args=[student_id])
    resp: Response = api_client.get(url)

    assert 200 == resp.status_code
    assert student_id == resp.json()["id"]


@pytest.mark.django_db
def test_get_student_by_id_unsuccessful(api_client: APIClient) -> None:

    url: str = reverse(STUDENT_DETAIL_URL, args=[1001])
    resp: Response = api_client.get(url)

    assert 404 == resp.status_code
    assert "Not Found" == resp.status_text


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload",
    [
        (
            {
                "school": 1,
                "title": "MR",
                "first_name": "John",
                "last_name": "John",
                "age": 10,
                "gender": "MALE",
            }
        ),
        (
            {
                "school": 2,
                "title": "MISS",
                "first_name": "Emma",
                "last_name": "Davies",
                "age": 12,
                "gender": "FEMALE",
            }
        ),
        (
            {
                "school": 3,
                "title": "MRS",
                "first_name": "Charlotte",
                "last_name": "Telles",
                "age": 13,
                "gender": "FEMALE",
            }
        ),
    ],
    ids=[
        "create-student-1-successful",
        "create-student-2-successful",
        "create-student-3-successful",
    ],
)
def test_create_student_successful(api_client: APIClient, payload: Dict) -> None:

    resp: Response = api_client.post(STUDENT_LIST_URL, data=payload)

    assert 201 == resp.status_code
    assert payload["first_name"] == resp.data["first_name"]
    print(resp.json())


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload",
    [
        (
            {
                "title": "MR",
                "first_name": "John",
                "last_name": "John",
                "age": 10,
                "gender": "MALE",
            }
        ),
        (
            {
                "title": "MISS",
                "first_name": "Emma",
                "last_name": "Davies",
                "age": 12,
                "gender": "FEMALE",
            }
        ),
        (
            {
                "title": "MRS",
                "first_name": "Charlotte",
                "last_name": "Telles",
                "age": 13,
                "gender": "FEMALE",
            }
        ),
    ],
    ids=[
        "create-student-1-unsuccessful-no-school",
        "create-student-2-unsuccessful-no-school",
        "create-student-3-unsuccessful-no-school",
    ],
)
def test_create_student_unsuccessful_no_school(
    api_client: APIClient, payload: Dict
) -> None:

    resp: Response = api_client.post(STUDENT_LIST_URL, data=payload)

    assert 400 == resp.status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload",
    [
        (
            {
                "school": 1,
                "title": "MR",
                "first_name": "John",
                "last_name": "John",
                "age": 9,
                "gender": "MALE",
            }
        ),
        (
            {
                "school": 2,
                "title": "MISS",
                "first_name": "Emma",
                "last_name": "Davies",
                "age": 22,
                "gender": "FEMALE",
            }
        ),
        (
            {
                "school": 1,
                "title": "MRS",
                "first_name": "Charlotte",
                "last_name": "Telles",
                "age": 30,
                "gender": "FEMALE",
            }
        ),
    ],
    ids=[
        "create-student-1-unsuccessful-age-validation",
        "create-student-2-unsuccessful-age-validation",
        "create-student-3-unsusccessful-age-validation",
    ],
)
def test_create_student_unsuccessful_age_validation(
    api_client: APIClient, payload: Dict
) -> None:

    resp: Response = api_client.post(STUDENT_LIST_URL, data=payload)

    assert 400 == resp.status_code
    assert "Students need to be age between 10 to 20 to register!" == resp.json()[0]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload",
    [
        (
            {
                "school": 1,
                "title": "MR",
                "first_name": "John",
                "last_name": "John",
                "age": 15,
                "gender": "MALE",
            }
        ),
        (
            {
                "school": 2,
                "title": "MISS",
                "first_name": "Emma",
                "last_name": "Davies",
                "age": 18,
                "gender": "FEMALE",
            }
        ),
        (
            {
                "school": 1,
                "title": "MRS",
                "first_name": "Charlotte",
                "last_name": "Telles",
                "age": 11,
                "gender": "FEMALE",
            }
        ),
    ],
    ids=[
        "create-student-1-unsuccessful-student_max_validation",
        "create-student-2-unsuccessful-student_max_validation",
        "create-student-3-unsusccessful-student_max_validation",
    ],
)
def test_create_student_unsuccessful_student_max_validation(
    api_client: APIClient, payload: Dict, get_id_for_full_school: int
) -> None:

    payload["school"] = get_id_for_full_school

    resp: Response = api_client.post(STUDENT_LIST_URL, data=payload)

    assert 400 == resp.status_code
    assert SCHOOL_FULL_ERROR_MESSAGE == resp.json()[0]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "student_id",
    [(1), (2)],
    ids=[
        "test-delete-1-successful",
        "test-delete-2-successful",
    ],
)
def test_delete_student_by_id_successful(
    api_client: APIClient, student_id: int
) -> None:

    url: str = reverse(STUDENT_DETAIL_URL, args=[student_id])
    resp: Response = api_client.delete(url)

    assert 204 == resp.status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "student_id",
    [(1000), (2000)],
    ids=[
        "test-delete-1-unsuccessful",
        "test-delete-2-unsuccessful",
    ],
)
def test_delete_student_by_id_unsuccessful(
    api_client: APIClient, student_id: int
) -> None:

    count = Student.objects.count()
    print(count)

    url: str = reverse(STUDENT_DETAIL_URL, args=[student_id])
    print(url)
    resp: Response = api_client.delete(url)

    assert 404 == resp.status_code
    assert "Not Found" == resp.status_text


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload,update_payload",
    [
        (
            {
                "school": 1,
                "title": "MRS",
                "first_name": "Charlotte",
                "last_name": "Telles",
                "age": 11,
                "gender": "FEMALE",
            },
            {
                "school": 1,
                "title": "MRS",
                "first_name": "Charlotte",
                "last_name": "Williams",
                "age": 11,
                "gender": "FEMALE",
            },
        ),
        (
            {
                "school": 1,
                "title": "MISS",
                "first_name": "Emma",
                "last_name": "Johns",
                "age": 11,
                "gender": "FEMALE",
            },
            {
                "school": 1,
                "title": "MRS",
                "first_name": "Emma",
                "last_name": "Marshall",
                "age": 11,
                "gender": "FEMALE",
            },
        ),
        (
            {
                "school": 1,
                "title": "MR",
                "first_name": "John",
                "last_name": "Davies",
                "age": 15,
                "gender": "MALE",
            },
            {
                "school": 2,
                "title": "MR",
                "first_name": "John",
                "last_name": "Davies",
                "age": 11,
                "gender": "MALE",
            },
        ),
    ],
    ids=[
        "test-update-studnet-surname-successful",
        "test-update-student-title-successful",
        "test-update-student-school-successful",
    ],
)
def test_update_student_successful(
    api_client: APIClient, payload: Dict, update_payload: Dict
) -> None:

    create_resp: Response = api_client.post(STUDENT_LIST_URL, data=payload)

    url: str = reverse(STUDENT_DETAIL_URL, args=[create_resp.data["id"]])
    resp: Response = api_client.put(url, data=update_payload)

    assert 200 == resp.status_code
    assert create_resp.data != resp.data


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload",
    [
        (
            {
                "school": 1,
                "title": "MISS",
                "first_name": "Sara",
                "last_name": "Telles",
                "age": 11,
                "gender": "FEMALE",
            }
        ),
    ],
    ids=[
        "test-update-studnet-school-full-unsuccessful",
    ],
)
def test_update_student_school_unsuccessful(
    api_client: APIClient, payload: Dict, get_id_for_full_school: int
) -> None:

    create_resp: Response = api_client.post(STUDENT_LIST_URL, data=payload)

    url: str = reverse(STUDENT_DETAIL_URL, args=[create_resp.data["id"]])
    payload["school"] = get_id_for_full_school
    resp: Response = api_client.put(url, data=payload)

    assert 400 == resp.status_code
    assert SCHOOL_FULL_ERROR_MESSAGE == resp.json()[0]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload,update_payload",
    [
        (
            {
                "school": 1,
                "title": "MRS",
                "first_name": "Charlotte",
                "last_name": "Telles",
                "age": 11,
                "gender": "FEMALE",
            },
            {
                "school": "",
                "title": "MRS",
                "first_name": "Charlotte",
                "last_name": "Williams",
                "age": 11,
                "gender": "FEMALE",
            },
        ),
        (
            {
                "school": 2,
                "title": "MR",
                "first_name": "John",
                "last_name": "John",
                "age": 14,
                "gender": "MALE",
            },
            {
                "title": "MR",
                "first_name": "John",
                "last_name": "John",
                "age": 14,
                "gender": "MALE",
            },
        ),
    ],
    ids=[
        "test-update-studnet-remove-school-empty-string-unsuccessful",
        "test-update-studnet-remove-school-exclude-unsuccessful",
    ],
)
def test_update_student_remove_school_unsuccessful(
    api_client: APIClient, payload: Dict, update_payload: Dict
) -> None:

    create_resp: Response = api_client.post(STUDENT_LIST_URL, data=payload)

    url: str = reverse(STUDENT_DETAIL_URL, args=[create_resp.data["id"]])
    resp: Response = api_client.put(url, data=update_payload)

    assert 400 == resp.status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "school_id,payload",
    [
        (1, {"first_name": 150}),
        (2, {"last_name": "Chon Buri"}),
        (3, {"school": 2}),
    ],
    ids=[
        "patch-successful-1",
        "patch-successful-2",
        "patch-successful-3",
    ],
)
def test_patch_student_successful(
    api_client: APIClient, school_id: int, payload: Dict
) -> None:

    url: str = reverse(STUDENT_DETAIL_URL, args=[school_id])
    resp: Response = api_client.patch(url, data=payload)

    assert 200 == resp.status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "school_id",
    [(3)],
    ids=["patch-change-school-unsuccessful"],
)
def test_patch_student_change_school_unsuccessful(
    api_client: APIClient, school_id: int, get_id_for_full_school: int
) -> None:

    url: str = reverse(STUDENT_DETAIL_URL, args=[school_id])
    payload: Dict = {"school": get_id_for_full_school}
    resp: Response = api_client.patch(url, data=payload)

    assert 400 == resp.status_code
    assert SCHOOL_FULL_ERROR_MESSAGE == resp.json()[0]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "school_id,payload",
    [
        (5, {"school": ""}),
    ],
    ids=["patch-remove-school-unsuccessful"],
)
def test_patch_student_remove_school_unsuccessful(
    api_client: APIClient, school_id: int, payload: Dict
) -> None:

    url: str = reverse(STUDENT_DETAIL_URL, args=[school_id])
    resp: Response = api_client.patch(url, data=payload)

    assert 400 == resp.status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "school_id,payload",
    [(5000, {"school": 1}), (10000, {"first_name": "John"})],
    ids=["patch-change-school-not-exist", "patch-change-name-not-exist"],
)
def test_patch_student_change_data_not_exist(
    api_client: APIClient, school_id: int, payload: Dict
) -> None:

    url: str = reverse(STUDENT_DETAIL_URL, args=[school_id])
    print(url)
    resp: Response = api_client.patch(url, data=payload)

    assert 404 == resp.status_code
    print(resp.json())

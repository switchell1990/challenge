from typing import Dict, OrderedDict

import pytest
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
from rest_framework.response import Response
from rest_framework.test import APIClient

from tests.conftest import SCHOOL_STUDENT_DETAIL_URL, SCHOOL_STUDENT_LIST_URL


@pytest.mark.django_db
@pytest.mark.parametrize(
    "school_id",
    [
        (1),
        (2),
        (3),
    ],
)
def test_get_school_student_list_successful(
    api_client: APIClient, school_id: int
) -> None:

    url: str = reverse(SCHOOL_STUDENT_LIST_URL, args=[school_id])
    resp: Response = api_client.get(url)

    assert 200 == resp.status_code
    assert isinstance(resp.data, OrderedDict)
    assert 5 == len(resp.json()["results"])


@pytest.mark.django_db
@pytest.mark.parametrize(
    "param_name,search_term",
    [
        ("first_name", lazy_fixture("get_student_first_name_data")),
        ("last_name", lazy_fixture("get_student_last_name_data")),
    ],
    ids=[
        "list-school-student-filter-first_name",
        "list-school-student-filter-last_name",
    ],
)
def test_school_student_list_with_filter(
    param_name: str, search_term: str, api_client: APIClient
) -> None:

    url: str = (
        f"{reverse(SCHOOL_STUDENT_LIST_URL, args=[1])}?{param_name}={search_term}"
    )
    resp: Response = api_client.get(url)

    assert 200 == resp.status_code
    assert search_term == resp.json()["results"][0][param_name]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload,school_id",
    [
        (
            {
                "title": "MR",
                "first_name": "John",
                "last_name": "Smith",
                "age": 10,
                "gender": "MALE",
            },
            1,
        ),
        (
            {
                "title": "MISS",
                "first_name": "Emma",
                "last_name": "Evans",
                "age": 12,
                "gender": "FEMALE",
            },
            2,
        ),
        (
            {
                "title": "MRS",
                "first_name": "Charlotte",
                "last_name": "Evans",
                "age": 13,
                "gender": "FEMALE",
            },
            3,
        ),
    ],
    ids=[
        "create-school-student-1-successful",
        "create-school-student-2-successful",
        "create-school-student-3-successful",
    ],
)
def test_create_school_student_successful(
    api_client: APIClient, payload: Dict, school_id: int
) -> None:

    url: str = reverse(SCHOOL_STUDENT_LIST_URL, args=[school_id])
    resp: Response = api_client.post(url, data=payload)

    assert 201 == resp.status_code
    assert payload["first_name"] == resp.data["first_name"]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload,school_id",
    [
        (
            {
                "first_name": "John",
                "last_name": "Smith",
                "age": 10,
                "gender": "MALE",
            },
            1,
        ),
        (
            {
                "title": "MISS",
                "first_name": "Emma",
                "age": 12,
                "gender": "FEMALE",
            },
            2,
        ),
    ],
    ids=[
        "create-school-student-1-unsuccessful",
        "create-school-student-2-unsuccessful",
    ],
)
def test_create_school_student_unsuccessful(
    api_client: APIClient, payload: Dict, school_id: int
) -> None:

    url: str = reverse(SCHOOL_STUDENT_LIST_URL, args=[school_id])
    resp: Response = api_client.post(url, data=payload)

    assert 400 == resp.status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload,school_id",
    [
        (
            {
                "title": "MR",
                "first_name": "John",
                "last_name": "John",
                "age": 9,
                "gender": "MALE",
            },
            1,
        ),
        (
            {
                "title": "MISS",
                "first_name": "Emma",
                "last_name": "Davies",
                "age": 22,
                "gender": "FEMALE",
            },
            2,
        ),
        (
            {
                "title": "MRS",
                "first_name": "Charlotte",
                "last_name": "Telles",
                "age": 30,
                "gender": "FEMALE",
            },
            3,
        ),
    ],
    ids=[
        "create-school-student-1-unsuccessful-age-validation",
        "create-school-student-2-unsuccessful-age-validation",
        "create-school-student-3-unsusccessful-age-validation",
    ],
)
def test_create_student_unsuccessful_age_validation(
    api_client: APIClient, payload: Dict, school_id: int
) -> None:

    url: str = reverse(SCHOOL_STUDENT_LIST_URL, args=[school_id])
    resp: Response = api_client.post(url, data=payload)

    assert 400 == resp.status_code
    assert "Students need to be age between 10 to 20 to register!" == resp.json()[0]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "school_id, student_id",
    [
        (1, 1),
        (1, 2),
        (1, 3),
    ],
    ids=[
        "test_get_school_student_id_successful-1",
        "test_get_school_student_id_successful-2",
        "test_get_school_student_id_successful-1",
    ],
)
def test_get_school_student_by_id_successful(
    api_client: APIClient, school_id: int, student_id: int
) -> None:

    url: str = reverse(SCHOOL_STUDENT_DETAIL_URL, args=[school_id, student_id])
    resp: Response = api_client.get(url)

    assert 200 == resp.status_code
    assert student_id == resp.json()["id"]
    assert school_id == resp.json()["school_details"]["id"]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "school_id, student_id",
    [
        (1, 1000),
        (1, 1001),
        (1, 1002),
    ],
)
def test_get_school_student_by_id_not_exist(
    api_client: APIClient, school_id: int, student_id: int
) -> None:

    url: str = reverse(SCHOOL_STUDENT_DETAIL_URL, args=[school_id, student_id])
    resp: Response = api_client.get(url)

    assert 404 == resp.status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload,update_payload,school_id",
    [
        (
            {
                "title": "MRS",
                "first_name": "Charlotte",
                "last_name": "Telles",
                "age": 11,
                "gender": "FEMALE",
            },
            {
                "title": "MRS",
                "first_name": "Charlotte",
                "last_name": "Williams",
                "age": 11,
                "gender": "FEMALE",
            },
            1,
        ),
        (
            {
                "title": "MISS",
                "first_name": "Emma",
                "last_name": "Johns",
                "age": 11,
                "gender": "FEMALE",
            },
            {
                "title": "MRS",
                "first_name": "Emma",
                "last_name": "Marshall",
                "age": 11,
                "gender": "FEMALE",
            },
            2,
        ),
        (
            {
                "title": "MR",
                "first_name": "John",
                "last_name": "Davies",
                "age": 15,
                "gender": "MALE",
            },
            {
                "title": "MR",
                "first_name": "John",
                "last_name": "Davies",
                "age": 15,
                "gender": "FEMALE",
            },
            3,
        ),
    ],
    ids=[
        "test-update-school-studnet-surname-successful",
        "test-update-school-student-title-successful",
        "test-update-school-student-gender-successful",
    ],
)
def test_update_school_student_successful(
    api_client: APIClient, payload: Dict, update_payload: Dict, school_id: int
) -> None:

    create_url: str = reverse(SCHOOL_STUDENT_LIST_URL, args=[school_id])
    create_resp: Response = api_client.post(create_url, data=payload)

    url: str = reverse(
        SCHOOL_STUDENT_DETAIL_URL, args=[school_id, create_resp.data["id"]]
    )
    resp: Response = api_client.put(url, data=update_payload)

    assert 200 == resp.status_code
    assert create_resp.data != resp.data


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload,update_payload,school_id",
    [
        (
            {
                "title": "MRS",
                "first_name": "Charlotte",
                "last_name": "Telles",
                "age": 11,
                "gender": "FEMALE",
            },
            {
                "title": "MRS",
                "first_name": "Charlotte",
                "age": 11,
                "gender": "FEMALE",
            },
            1,
        ),
        (
            {
                "title": "MISS",
                "first_name": "Emma",
                "last_name": "Johns",
                "age": 11,
                "gender": "FEMALE",
            },
            {
                "first_name": "Emma",
                "last_name": "Marshall",
                "age": 11,
                "gender": "FEMALE",
            },
            2,
        ),
    ],
    ids=[
        "test-update-school-studnet-missing-surname-unsuccessful",
        "test-update-school-student-missing-title-unsuccessful",
    ],
)
def test_update_school_student_missing_data_unsuccessful(
    api_client: APIClient, payload: Dict, update_payload: Dict, school_id: int
) -> None:

    create_url: str = reverse(SCHOOL_STUDENT_LIST_URL, args=[school_id])
    create_resp: Response = api_client.post(create_url, data=payload)

    url: str = reverse(
        SCHOOL_STUDENT_DETAIL_URL, args=[school_id, create_resp.data["id"]]
    )
    resp: Response = api_client.put(url, data=update_payload)

    assert 400 == resp.status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "update_payload,school_id,student_id",
    [
        (
            {
                "title": "MRS",
                "first_name": "Charlotte",
                "last_name": "Telles",
                "age": 11,
                "gender": "FEMALE",
            },
            1,
            1000,
        ),
        (
            {
                "title": "MISS",
                "first_name": "Emma",
                "last_name": "Marshall",
                "age": 11,
                "gender": "FEMALE",
            },
            2,
            10001,
        ),
    ],
    ids=[
        "test-update-school-studnet-missing-surname-unsuccessful",
        "test-update-school-student-missing-title-unsuccessful",
    ],
)
def test_update_school_student_id_not_exist(
    api_client: APIClient, update_payload: Dict, school_id: int, student_id: int
) -> None:

    url: str = reverse(SCHOOL_STUDENT_DETAIL_URL, args=[school_id, student_id])
    resp: Response = api_client.put(url, data=update_payload)

    assert 404 == resp.status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "school_id,payload,student_id",
    [
        (1, {"first_name": 150}, 1),
        (1, {"last_name": "Chon Buri"}, 2),
        (1, {"title": "MISS"}, 3),
    ],
    ids=[
        "patch-successful-1",
        "patch-successful-2",
        "patch-successful-3",
    ],
)
def test_patch_school_student_successful(
    api_client: APIClient, school_id: int, payload: Dict, student_id: int
) -> None:

    url: str = reverse(SCHOOL_STUDENT_DETAIL_URL, args=[school_id, student_id])
    resp: Response = api_client.patch(url, data=payload)

    assert 200 == resp.status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "school_id,payload,student_id",
    [(1, {"title": "MR"}, 1000), (2, {"first_name": "John"}, 1001)],
    ids=["patch-change-title-not-exist", "patch-change-name-not-exist"],
)
def test_patch_student_change_data_not_exist(
    api_client: APIClient, school_id: int, payload: Dict, student_id: int
) -> None:

    url: str = reverse(SCHOOL_STUDENT_DETAIL_URL, args=[school_id, student_id])
    resp: Response = api_client.patch(url, data=payload)

    assert 404 == resp.status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "school_id,student_id",
    [(1, 1), (1, 2)],
    ids=[
        "test-school-student-delete-1-successful",
        "test-school-student-delete-2-successful",
    ],
)
def test_delete_school_student_by_id_successful(
    api_client: APIClient, school_id: int, student_id: int
) -> None:

    url: str = reverse(SCHOOL_STUDENT_DETAIL_URL, args=[school_id, student_id])
    resp: Response = api_client.delete(url)

    assert 204 == resp.status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "school_id,student_id",
    [(1, 1000), (1, 2000)],
    ids=[
        "test-school-student-delete-1-not-exist",
        "test-school-student-delete-2-not-exist",
    ],
)
def test_delete_school_student_by_id_not_exist(
    api_client: APIClient, school_id: int, student_id: int
) -> None:

    url: str = reverse(SCHOOL_STUDENT_DETAIL_URL, args=[school_id, student_id])
    resp: Response = api_client.delete(url)

    assert 404 == resp.status_code
    assert "Not Found" == resp.status_text

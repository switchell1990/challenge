from typing import Dict

import pytest
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
from rest_framework.response import Response
from rest_framework.test import APIClient

from tests.conftest import SCHOOL_DETAIL_URL, SCHOOL_LIST_URL


@pytest.mark.django_db
def test_school_list_successful(api_client: APIClient) -> None:

    resp: Response = api_client.get(SCHOOL_LIST_URL)

    assert 200 == resp.status_code
    assert 10 == len(resp.json()["results"])


@pytest.mark.django_db
@pytest.mark.parametrize(
    "param_name,search_term",
    [
        ("name", lazy_fixture("get_school_name_data")),
        ("location", lazy_fixture("get_school_location_data")),
    ],
    ids=[
        "list-school-filter-name",
        "list-school-filter-location",
    ],
)
def test_school_list_with_filter(
    param_name: str, search_term: str, api_client: APIClient
) -> None:

    url: str = f"{SCHOOL_LIST_URL}?{param_name}={search_term}"
    resp: Response = api_client.get(url)

    assert 200 == resp.status_code
    assert 1 == len(resp.json()["results"])
    assert search_term == resp.json()["results"][0][param_name]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "school_id",
    [(1), (2), (3)],
    ids=[
        "get-school-1-successful",
        "get-school-2-successful",
        "get-school-3-successful",
    ],
)
def test_get_school_by_id_successful(school_id: int, api_client: APIClient) -> None:

    url: str = reverse(SCHOOL_DETAIL_URL, args=[school_id])
    resp: Response = api_client.get(url)

    assert 200 == resp.status_code
    assert school_id == resp.json()["id"]


@pytest.mark.django_db
def test_get_school_by_id_unsuccessful(api_client: APIClient) -> None:

    url: str = reverse(SCHOOL_DETAIL_URL, args=[300])
    resp: Response = api_client.get(url)

    assert 404 == resp.status_code
    assert "Not Found" == resp.status_text


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload",
    [
        (
            {
                "name": "Martin School",
                "code": "A01234",
                "location": "Bangkok",
                "student_max_number": 10,
            }
        ),
        (
            {
                "name": "John School",
                "code": "A01235",
                "location": "Bangkok",
                "student_max_number": 15,
            }
        ),
        (
            {
                "name": "Marys School",
                "code": "A01236",
                "location": "Chiang Mai",
                "student_max_number": 30,
            }
        ),
    ],
    ids=[
        "create-school-1",
        "create-school-2",
        "create-school-3",
    ],
)
def test_create_school_successful(api_client: APIClient, payload: Dict) -> None:

    resp: Response = api_client.post(SCHOOL_LIST_URL, data=payload)

    print(resp.status_code)
    assert 201 == resp.status_code
    assert payload["name"] == resp.data["name"]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload",
    [
        (
            {
                "code": "A01234",
                "location": "Bangkok",
                "student_max_number": 10,
            }
        ),
        (
            {
                "name": "John School",
                "location": "Bangkok",
                "student_max_number": 15,
            }
        ),
        (
            {
                "name": "Marys School",
                "code": "A01236",
            }
        ),
    ],
    ids=[
        "create-school-1-unsuccessful",
        "create-school-2-unsuccessful",
        "create-school-3-unsuccessful",
    ],
)
def test_create_school_unsuccessful(api_client: APIClient, payload: Dict) -> None:

    resp: Response = api_client.post(SCHOOL_LIST_URL, data=payload)

    assert 400 == resp.status_code
    assert "Bad Request" == resp.status_text


@pytest.mark.django_db
@pytest.mark.parametrize(
    "school_id",
    [
        (1),
        (2),
    ],
    ids=[
        "delete-school-1-successful",
        "delete-school-2-successful",
    ],
)
def test_delete_school_successful(api_client: APIClient, school_id: int) -> None:

    url: str = reverse(SCHOOL_DETAIL_URL, args=[school_id])
    resp: Response = api_client.delete(url)

    assert 204 == resp.status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "school_id",
    [
        (1000),
        (500),
    ],
    ids=[
        "delete-school-1-unsuccessful",
        "delete-school-2-unsuccessful",
    ],
)
def test_delete_school_unsuccessful(api_client: APIClient, school_id: int) -> None:

    url: str = reverse(SCHOOL_DETAIL_URL, args=[school_id])
    resp: Response = api_client.delete(url)

    assert 404 == resp.status_code
    assert "Not Found" == resp.status_text


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload,update_payload",
    [
        (
            {
                "name": "Martin School",
                "code": "A01234",
                "location": "Bangkok",
                "student_max_number": 10,
            },
            {
                "name": "Martin School",
                "code": "A01234",
                "location": "Chiang Mai",
                "student_max_number": 10,
            },
        ),
        (
            {
                "name": "John School",
                "code": "A01235",
                "location": "Bangkok",
                "student_max_number": 15,
            },
            {
                "name": "John School",
                "code": "A01235",
                "location": "Bangkok",
                "student_max_number": 55,
            },
        ),
    ],
    ids=[
        "test-update-successful-1",
        "test-update-successful-2",
    ],
)
def test_update_school_successful(
    api_client: APIClient, payload: Dict, update_payload: Dict
) -> None:

    create_resp: Response = api_client.post(SCHOOL_LIST_URL, data=payload)

    url: str = reverse(SCHOOL_DETAIL_URL, args=[create_resp.data["id"]])
    resp: Response = api_client.put(url, data=update_payload)

    assert 200 == resp.status_code
    assert create_resp.data != resp.data


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload,update_payload",
    [
        (
            {
                "name": "Martin School",
                "code": "A01234",
                "location": "Bangkok",
                "student_max_number": 10,
            },
            {
                "name": "Martin School",
                "location": "Chiang Mai",
                "student_max_number": 10,
            },
        ),
        (
            {
                "name": "John School",
                "code": "A01235",
                "location": "Bangkok",
                "student_max_number": 15,
            },
            {
                "name": "John School",
                "code": "A01235",
                "student_max_number": 55,
            },
        ),
    ],
    ids=[
        "test-update-unsuccessful-1",
        "test-update-unsuccessful-2",
    ],
)
def test_update_school_unsuccessful(
    api_client: APIClient, payload: Dict, update_payload: Dict
) -> None:

    create_resp: Response = api_client.post(SCHOOL_LIST_URL, data=payload)

    url: str = reverse(SCHOOL_DETAIL_URL, args=[create_resp.data["id"]])
    resp: Response = api_client.put(url, data=update_payload)

    assert 400 == resp.status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "school_id,payload",
    [
        (
            1,
            {
                "student_max_number": 150,
            },
        ),
        (
            2,
            {
                "location": "Chon Buri",
            },
        ),
    ],
    ids=[
        "patch-successful-1",
        "patch-successful-2",
    ],
)
def test_patch_school_successful(
    api_client: APIClient, school_id: int, payload: Dict
) -> None:

    url: str = reverse(SCHOOL_DETAIL_URL, args=[school_id])
    resp: Response = api_client.patch(url, data=payload)

    assert 200 == resp.status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    "school_id,payload",
    [
        (
            1000,
            {
                "student_max_number": 150,
            },
        ),
        (
            5333,
            {
                "location": "Chon Buri",
            },
        ),
    ],
    ids=[
        "patch-unsuccessful-1",
        "patch-unsuccessful-2",
    ],
)
def test_patch_school_unsuccessful(
    api_client: APIClient,
    school_id: int,
    payload: Dict,
) -> None:

    url: str = reverse(SCHOOL_DETAIL_URL, args=[school_id])
    resp: Response = api_client.patch(url, data=payload)

    assert 404 == resp.status_code

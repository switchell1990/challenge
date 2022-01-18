from typing import List

from django.urls import include, path
from rest_framework_nested.routers import NestedDefaultRouter, SimpleRouter

from core.views import SchoolViewSet, StudentNestedViewSet, StudentViewSet

app_name: str = "api"

router: SimpleRouter = SimpleRouter()
router.register(r"schools", SchoolViewSet, basename="schools")
router.register(r"students", StudentViewSet, basename="students")

# Nested Routes
student_router: NestedDefaultRouter = NestedDefaultRouter(
    router, r"schools", lookup="school"
)
student_router.register(r"students", StudentNestedViewSet, basename="school-students")

urlpatterns: List = [
    path("", include(router.urls)),
    path("", include(student_router.urls)),
]

from typing import List

from django.contrib import admin
from django.urls import include, path
from rest_framework.documentation import include_docs_urls

urlpatterns: List = [
    path("admin/", admin.site.urls),
    path("api/", include("core.urls", namespace="api")),
    path(r"docs/", include_docs_urls(title="Mantal School API")),
]

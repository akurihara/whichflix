from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from whatshouldwewatch.elections.views import ElectionsView

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    # Elections
    path("v1/elections", ElectionsView.as_view(), name="elections"),
    # Open API schema
    path(
        "openapi",
        get_schema_view(
            title="WhatShouldWeWatch",
            description="What Should We Watch",
            version="1.0.0",
        ),
        name="openapi_schema",
    ),
    # ReDoc template for Open API schema
    path(
        "redoc/",
        TemplateView.as_view(
            template_name="redoc.html", extra_context={"schema_url": "openapi_schema"}
        ),
        name="redoc",
    ),
]

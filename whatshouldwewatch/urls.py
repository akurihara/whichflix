from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from whatshouldwewatch.elections.views import (
    CandidatesView,
    ElectionsView,
    ElectionDetailView,
    ParticipantsView,
)

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    # Elections
    path("v1/elections", ElectionsView.as_view(), name="elections"),
    path(
        "v1/elections/<slug:election_id>",
        ElectionDetailView.as_view(),
        name="election_detail",
    ),
    path(
        "v1/elections/<slug:election_id>/candidates",
        CandidatesView.as_view(),
        name="candidates",
    ),
    path(
        "v1/elections/<slug:election_id>/participants",
        ParticipantsView.as_view(),
        name="participants",
    ),
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

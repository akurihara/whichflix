from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from whatshouldwewatch.elections.views import (
    CandidatesView,
    ElectionsView,
    ElectionDetailView,
    ParticipantsView,
    VotesView,
)

# https://drf-yasg.readthedocs.io/en/latest/readme.html#quickstart
api_info = openapi.Info(
    title="WhichFlix",
    description="The premier app for choosing a movie to watch!",
    default_version="1.0.0",
)
schema_view = get_schema_view(public=True, permission_classes=(permissions.AllowAny,))

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    # Elections
    path("v1/candidates/<slug:candidate_id>/votes", VotesView.as_view(), name="votes"),
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
    path("openapi", schema_view.without_ui(cache_timeout=0), name="openapi_schema"),
    path(
        "redoc/",
        TemplateView.as_view(
            template_name="redoc.html", extra_context={"schema_url": "openapi_schema"}
        ),
        name="redoc",
    ),
]

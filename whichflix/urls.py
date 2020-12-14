import django_eventstream
from django.conf.urls import include
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django.views.generic import TemplateView
from django_eventstream import send_event
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from whichflix.elections.views import (
    CandidatesView,
    ElectionsView,
    ElectionDetailView,
    ParticipantsView,
    VotesView,
)
from whichflix.movies.views import MoviesSearchView

# https://drf-yasg.readthedocs.io/en/latest/readme.html#quickstart
api_info = openapi.Info(
    title="WhichFlix",
    description="The premier app for choosing a movie to watch!",
    default_version="1.0.0",
)
schema_view = get_schema_view(public=True, permission_classes=(permissions.AllowAny,))


def trigger_error(request):
    division_by_zero = 1 / 0
    print(division_by_zero)


def send_test_event(request):
    channel = request.GET.get("channel") or "test"
    send_event(channel, "message", {"text": "hello world"})
    return JsonResponse({"channel": channel}, status=200)


urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    # Elections
    path("v1/candidates/<slug:candidate_id>/votes/", VotesView.as_view(), name="votes"),
    path("v1/elections/", ElectionsView.as_view(), name="elections"),
    path(
        "v1/elections/<slug:election_id>/",
        ElectionDetailView.as_view(),
        name="election_detail",
    ),
    path(
        "v1/elections/<slug:election_id>/candidates/",
        CandidatesView.as_view(),
        name="candidates",
    ),
    path(
        "v1/elections/<slug:election_id>/participants/",
        ParticipantsView.as_view(),
        name="participants",
    ),
    # Movies
    path("v1/movies/search/", MoviesSearchView.as_view(), name="movies_search"),
    # django-eventstream
    path(
        "v1/elections/<slug:election_id>/events/",
        include(django_eventstream.urls),
        {"format-channels": ["election-{election_id}"]},
    ),
    path("events/", include(django_eventstream.urls), {"channels": ["test"]}),
    path("events-debug/", send_test_event),  # TODO: remove eventually
    # Open API schema
    path("openapi/", schema_view.without_ui(cache_timeout=0), name="openapi_schema"),
    path(
        "redoc/",
        TemplateView.as_view(
            template_name="redoc.html", extra_context={"schema_url": "openapi_schema"}
        ),
        name="redoc",
    ),
    # Sentry testing
    path("sentry-debug/", trigger_error),
]

import json
from unittest.mock import patch
from urllib.parse import urlencode

import fakeredis
import responses
from django.urls import reverse
from rest_framework.test import APITestCase

from test import factories
from test.movies import fixtures
from whichflix.movies import constants


class TestMoviesSearchView(APITestCase):
    def setUp(self):
        self.url = reverse("movies_search")

        # Redis
        self.redis_patcher = patch(
            "whichflix.movies.manager.redis_client", fakeredis.FakeStrictRedis()
        )
        self.redis_mock = self.redis_patcher.start()

    def tearDown(self):
        # Redis
        self.redis_patcher.stop()

    @responses.activate
    def test_get(self):
        responses.add(
            responses.GET,
            "https://api.themoviedb.org/3/search/movie",
            json=fixtures.SEARCH_MOVIES_RESPONSE,
            status=200,
        )
        responses.add(
            responses.GET,
            "https://api.themoviedb.org/3/configuration",
            json=fixtures.CONFIGURATION_RESPONSE,
            status=200,
        )

        parameters = urlencode({"query": "The Matrix"})
        url = "{base_url}?{parameters}".format(base_url=self.url, parameters=parameters)
        response = self.client.get(url)

        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), fixtures.EXPECTED_RESPONSE_SEARCH_MOVIES)

    @responses.activate
    def test_get_uses_cached_tmdb_configuration_if_present(self):
        responses.add(
            responses.GET,
            "https://api.themoviedb.org/3/search/movie",
            json=fixtures.SEARCH_MOVIES_RESPONSE,
            status=200,
        )
        self.redis_mock.set(
            constants.TMDB_CONFIGURATION_KEY,
            json.dumps(fixtures.CONFIGURATION_RESPONSE),
        )

        parameters = urlencode({"query": "The Matrix"})
        url = "{base_url}?{parameters}".format(base_url=self.url, parameters=parameters)
        response = self.client.get(url)

        # Verify response.
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), fixtures.EXPECTED_RESPONSE_SEARCH_MOVIES)


class TestGetMovieDetailView(APITestCase):
    def setUp(self):
        # Redis
        self.redis_patcher = patch(
            "whichflix.movies.manager.redis_client", fakeredis.FakeStrictRedis()
        )
        self.redis_mock = self.redis_patcher.start()

    def tearDown(self):
        # Redis
        self.redis_patcher.stop()

    def skip_test_get_stores_movie_in_redis_cache(self):
        movie = factories.create_movie(provider_id="123")
        url = reverse("movie_detail", kwargs={"movie_id": movie.id})
        response = self.client.get(url)

        # Verify response.
        self.assertEqual(response.status_code, 200)

    def skip_test_get_reads_movie_from_redis_cache(self):
        movie = factories.create_movie(provider_id="123")
        url = reverse("movie_detail", kwargs={"movie_id": movie.id})
        response = self.client.get(url)

        # Verify response.
        self.assertEqual(response.status_code, 200)

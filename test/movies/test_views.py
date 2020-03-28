from urllib.parse import urlencode

from django.urls import reverse
from rest_framework.test import APITestCase


class TestMoviesSearchView(APITestCase):
    def setUp(self):
        self.url = reverse("movies_search")

    def test_get(self):
        parameters = urlencode({"query": "The Matrix"})
        url = "{base_url}?{parameters}".format(base_url=self.url, parameters=parameters)
        response = self.client.get(url)

        # Verify response.
        self.assertEqual(response.status_code, 200)

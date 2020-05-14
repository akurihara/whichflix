import copy
from dataclasses import dataclass
from typing import List

from django.db import models

from whichflix.movies import constants


class Movie(models.Model):
    provider_slug = models.CharField(
        max_length=255, choices=constants.MOVIE_PROVIDER_CHOICES.items()
    )
    provider_id = models.CharField(max_length=255)

    class Meta:
        unique_together = (("provider_id", "provider_slug"),)
        index_together = (("provider_id", "provider_slug"),)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "Movie: {}".format(self.id)


@dataclass
class TMDBMovie:
    _id: int
    title: str
    overview: str
    release_date: str
    poster_path: str
    genre_ids: List[int]

    @classmethod
    def from_tmdb_result(cls, result: dict) -> "TMDBMovie":
        return cls(
            _id=result["id"],
            title=result["title"],
            overview=result["overview"],
            release_date=result["release_date"],
            poster_path=result["poster_path"],
            genre_ids=copy.deepcopy(result["genre_ids"]),
        )

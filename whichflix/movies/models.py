import copy
from dataclasses import dataclass
from typing import List


@dataclass
class TMDBMovie:
    _id: int
    title: str
    overview: str
    release_date: str
    poster_path: str
    genre_ids: List[int]

    @classmethod
    def from_tmdb_movie_result(cls, result: dict) -> "TMDBMovie":
        return cls(
            _id=result["id"],
            title=result["title"],
            overview=result["overview"],
            release_date=result["release_date"],
            poster_path=result["poster_path"],
            genre_ids=copy.deepcopy(result["genre_ids"]),
        )

    @classmethod
    def from_tmdb_movie_info(cls, info: dict) -> "TMDBMovie":
        return cls(
            _id=info["id"],
            title=info["title"],
            overview=info["overview"],
            release_date=info["release_date"],
            poster_path=info["poster_path"],
            genre_ids=[genre["id"] for genre in info["genres"]],
        )

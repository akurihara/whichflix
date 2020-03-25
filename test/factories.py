from typing import Optional

from whichflix.elections.models import Candidate, Election, Participant
from whichflix.movies import constants as movie_constants
from whichflix.movies.models import Movie
from whichflix.users.models import Device


def create_device(device_token: Optional[str] = None) -> Device:
    device_token = device_token or "abc123"
    device = Device.objects.create(device_token=device_token)

    return device


def create_election(
    device: Optional[Device] = None, external_id: Optional[str] = None
) -> Election:
    device = device or create_device()
    external_id = external_id or "abc123"
    election = Election.objects.create(
        title="Movie night in Brooklyn!", external_id=external_id
    )
    Participant.objects.create(
        name="John", election=election, device=device, is_initiator=True
    )

    return election


def create_movie(provider_id: Optional[str] = None) -> Movie:
    provider_id = provider_id or "abc123"
    movie = Movie.objects.create(
        provider_slug=movie_constants.MOVIE_PROVIDER_THE_MOVIE_DB,
        provider_id=provider_id,
    )

    return movie


def create_candidate(
    election: Election, participant: Participant, movie: Optional[Movie] = None
) -> Movie:
    movie = movie or create_movie()
    candidate = Candidate.objects.create(
        election=election, participant=participant, movie=movie
    )

    return candidate

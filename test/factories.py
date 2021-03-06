import datetime
from typing import Optional

from django.utils import timezone

from whichflix.elections.models import Candidate, Election, Participant
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


def create_participant(
    election: Election,
    device: Device,
    name: Optional[str] = None,
    is_deleted: bool = False,
) -> Participant:
    name = name or "Jane"
    participant = Participant.objects.create(
        name=name, election=election, device=device, is_initiator=False
    )

    if is_deleted:
        participant.deleted_at = datetime.datetime.now(tz=timezone.utc)
        participant.save()

    return participant


def create_candidate(
    election: Election, participant: Participant, movie_id: Optional[str] = None
) -> Candidate:
    movie_id = movie_id or "603"
    candidate = Candidate.objects.create(
        election=election, participant=participant, movie_id=movie_id
    )

    return candidate

from typing import Optional

from whatshouldwewatch.elections.models import Candidate, Election, Participant
from whatshouldwewatch.movies.models import Movie
from whatshouldwewatch.users.models import Device
from whatshouldwewatch.utils import generate_external_id


def initiate_election(
    device: Device, initiator_name: str, election_description: Device
) -> Election:
    election = _create_election(election_description)
    _create_participant_who_initiated_election(election, device, initiator_name)

    return election


def _create_election(description: str) -> Election:
    election = Election.objects.create(description=description)
    election.external_id = generate_external_id(election.id)
    election.save()

    return election


def _create_participant_who_initiated_election(
    election: Election, device: Device, name: str
) -> Participant:
    participant = Participant.objects.create(
        name=name, election=election, device=device, is_initiator=True
    )

    return participant


def create_participant_for_election(
    election: Election, device: Device, name: str
) -> Participant:
    participant = Participant.objects.create(
        name=name, election=election, device=device, is_initiator=False
    )

    return participant


def get_participant_by_device_token(device_token: str) -> Optional[Participant]:
    try:
        participant = Participant.objects.get(device__device_token=device_token)
    except Participant.DoesNotExist:
        participant = None

    return participant


def create_candidate_for_election(
    election: Election, participant: Participant, movie: Movie
) -> Candidate:
    pass

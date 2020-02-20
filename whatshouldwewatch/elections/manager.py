from whatshouldwewatch.elections.models import Election, Participant
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

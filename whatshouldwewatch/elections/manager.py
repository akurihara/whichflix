from whatshouldwewatch.elections.models import Election
from whatshouldwewatch.users.models import Device
from whatshouldwewatch.utils import generate_external_id


def create_election_for_device(description: str, initiator: Device) -> Election:
    election = Election.objects.create(description=description, initiator=initiator)
    election.external_id = generate_external_id(election.id)
    election.save()

    return election

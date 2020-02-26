from typing import Optional

from whatshouldwewatch.elections import errors
from whatshouldwewatch.elections.models import Candidate, Election, Participant, Vote
from whatshouldwewatch.movies.models import Movie
from whatshouldwewatch.users.models import Device
from whatshouldwewatch.utils import generate_external_id


def get_election_and_related_objects(election_id: str) -> Optional[Election]:
    election = (
        Election.objects.prefetch_related(
            "participants", "candidates", "candidates__votes"
        )
        .filter(external_id=election_id)
        .first()
    )

    return election


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
    _validate_participant_is_in_election(participant, election)
    _validate_candidate_does_not_already_exist(movie, election)

    candidate = Candidate.objects.create(
        participant=participant, movie=movie, election=election
    )

    return candidate


def _validate_participant_is_in_election(
    participant: Participant, election: Election
) -> None:
    if participant.election != election:
        raise errors.ParticipantNotPartOfElectionError()


def _validate_candidate_does_not_already_exist(
    movie: Movie, election: Election
) -> None:
    if election.candidates.filter(movie=movie).exists():
        raise errors.CandidateAlreadyExistsError()


def cast_vote_for_candidate(participant: Participant, candidate: Candidate) -> Vote:
    _validate_participant_is_in_election(participant, candidate.election)
    _validate_participant_has_not_already_voted_for_candidate(participant, candidate)

    vote = Vote.objects.create(participant=participant, candidate=candidate)

    return vote


def _validate_participant_has_not_already_voted_for_candidate(
    participant: Participant, candidate: Candidate
) -> None:
    if candidate.votes.filter(participant=participant).exists():
        raise errors.ParticipantAlreadyVotedForCandidate

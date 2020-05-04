import datetime

from django.utils import timezone
from typing import List, Optional

from whichflix.elections import errors
from whichflix.elections.models import Candidate, Election, Participant, Vote
from whichflix.movies.models import Movie
from whichflix.users.models import Device
from whichflix.utils import generate_external_id


#
# Elections
#


def get_election_and_related_objects(election_id: str) -> Optional[Election]:
    election = (
        Election.objects.prefetch_related(
            "participants", "candidates", "candidates__votes"
        )
        .filter(external_id=election_id)
        .first()
    )

    return election


def get_elections_and_related_objects_by_device_token(
    device_token: str,
) -> List[Election]:
    elections = (
        Election.objects.prefetch_related(
            "participants", "candidates", "candidates__votes"
        )
        .filter(
            participants__device__device_token=device_token,
            participants__deleted_at__isnull=True,
        )
        .order_by("id")
        .all()
    )

    return elections


def initiate_election(device: Device, initiator_name: str, title: str) -> Election:
    election = _create_election(title)
    _create_participant_who_initiated_election(election, device, initiator_name)

    return election


def _create_election(title: str) -> Election:
    election = Election.objects.create(title=title)
    election.external_id = generate_external_id(election.id)
    election.save()

    return election


def update_election(election: Election, device_token: str, title: str) -> Election:
    _validate_device_is_initiator_of_election(election, device_token)

    election.title = title
    election.save()

    return election


def _validate_device_is_initiator_of_election(
    election: Election, device_token: str
) -> None:
    did_device_initiate_election = (
        Participant.objects.filter(device__device_token=device_token)
        .filter(election=election)
        .exists()
    )

    if not did_device_initiate_election:
        raise errors.DeviceDidNotInitiateElectionError()


def _create_participant_who_initiated_election(
    election: Election, device: Device, name: str
) -> Participant:
    participant = Participant.objects.create(
        name=name, election=election, device=device, is_initiator=True
    )

    return participant


def get_candidate_actions_map_for_election(
    election: Election, participant: Participant
) -> dict:
    return {
        candidate.id: get_candidate_actions_for_participant(candidate, participant)
        for candidate in election.candidates.all()
    }


#
# Participants
#


def create_or_activate_participant_for_election(
    election: Election, device: Device, name: str
) -> Participant:
    participant = _get_deleted_participant_by_election_and_device_token(
        election, device.device_token
    )

    if participant is not None:
        participant.deleted_at = None
        participant.name = name
        participant.save()
    else:
        participant = create_participant_for_election(election, device, name)

    return participant


def create_participant_for_election(
    election: Election, device: Device, name: str
) -> Participant:
    participant = Participant.objects.create(
        name=name, election=election, device=device, is_initiator=False
    )

    return participant


def get_participant_by_election_and_device_token(
    election: Election, device_token: str
) -> Optional[Participant]:
    try:
        participant = Participant.objects.get(
            election=election,
            device__device_token=device_token,
            deleted_at__isnull=True,
        )
    except Participant.DoesNotExist:
        participant = None

    return participant


def _get_deleted_participant_by_election_and_device_token(
    election: Election, device_token: str
) -> Optional[Participant]:
    try:
        participant = Participant.objects.get(
            election=election,
            device__device_token=device_token,
            deleted_at__isnull=False,
        )
    except Participant.DoesNotExist:
        participant = None

    return participant


def delete_participant(participant: Participant) -> Participant:
    if participant.deleted_at is None:
        participant.deleted_at = datetime.datetime.now(tz=timezone.utc)

    participant.save()

    return participant


#
# Candidates
#


def get_candidate_and_related_objects(candidate_id: int) -> Optional[Candidate]:
    election = (
        Candidate.objects.prefetch_related("movie", "votes", "votes__participant")
        .filter(id=candidate_id)
        .first()
    )

    return election


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


def get_candidate_actions_for_participant(
    candidate: Candidate, participant: Participant
) -> dict:
    has_participant_voted_for_candidate = candidate.votes.filter(
        participant=participant, deleted_at__isnull=True
    ).exists()
    did_participant_create_candidate = candidate.participant.id == participant.id

    return {
        "can_vote": not has_participant_voted_for_candidate,
        "can_remove_vote": has_participant_voted_for_candidate,
        "can_delete": did_participant_create_candidate,
    }


#
# Votes
#


def create_or_activate_vote_for_candidate(
    participant: Participant, candidate: Candidate
) -> Vote:
    vote = _get_deleted_vote_by_candidate_and_participant(participant, candidate)

    if vote is not None:
        vote.deleted_at = None
        vote.save()
    else:
        vote = _create_vote_for_candidate(participant, candidate)

    return vote


def _create_vote_for_candidate(participant: Participant, candidate: Candidate) -> Vote:
    _validate_participant_is_in_election(participant, candidate.election)
    _validate_participant_has_not_already_voted_for_candidate(participant, candidate)

    vote = Vote.objects.create(participant=participant, candidate=candidate)

    return vote


def _validate_participant_has_not_already_voted_for_candidate(
    participant: Participant, candidate: Candidate
) -> None:
    if candidate.votes.filter(participant=participant).exists():
        raise errors.ParticipantAlreadyVotedForCandidate


def get_vote_by_participant_and_candidate(
    participant: Participant, candidate: Candidate
) -> Optional[Vote]:
    try:
        vote = Vote.objects.get(
            candidate=candidate, participant=participant, deleted_at__isnull=True
        )
    except Vote.DoesNotExist:
        vote = None

    return vote


def _get_deleted_vote_by_candidate_and_participant(
    participant: Participant, candidate: Candidate
) -> Optional[Vote]:
    try:
        vote = Vote.objects.get(
            candidate=candidate, participant=participant, deleted_at__isnull=False
        )
    except Vote.DoesNotExist:
        vote = None

    return vote


def delete_vote(vote: Vote) -> Vote:
    if vote.deleted_at is None:
        vote.deleted_at = datetime.datetime.now(tz=timezone.utc)

    vote.save()

    return vote

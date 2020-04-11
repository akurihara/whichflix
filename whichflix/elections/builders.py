from typing import List

from whichflix.elections.models import Candidate, Election, Participant
from whichflix.movies import builders as movie_builders


def build_election_document(election: Election) -> dict:
    return {
        "id": election.external_id,
        "title": election.title,
        "created_at": election.created_at.isoformat(),
        "participants": _build_participant_documents_for_election(election),
        "candidates": _build_candidate_documents_for_election(election),
    }


def _build_paticipant_document(participant: Participant) -> dict:
    return {
        "id": str(participant.id),
        "name": participant.name,
        "is_initiator": participant.is_initiator,
    }


def _build_participant_documents_for_election(election: Election) -> List[dict]:
    return [
        _build_paticipant_document(participant)
        for participant in election.participants.order_by("id").order_by("name").all()
        if participant.deleted_at is None
    ]


def build_candidate_document(candidate: Candidate) -> dict:
    return {
        "id": str(candidate.id),
        "movie": movie_builders.build_movie_document(candidate.movie),
        "vote_count": candidate.votes.filter(
            participant__deleted_at__isnull=True, deleted_at__isnull=True
        ).count(),
        "voting_participants": [
            _build_paticipant_document(vote.participant)
            for vote in candidate.votes.filter(
                participant__deleted_at__isnull=True, deleted_at__isnull=True
            ).all()
        ],
    }


def _build_candidate_documents_for_election(election: Election) -> List[dict]:
    return [
        build_candidate_document(candidate) for candidate in election.candidates.all()
    ]

from typing import List, Optional

from whichflix.elections.models import Candidate, Election, Participant
from whichflix.movies import builders as movie_builders


def build_election_document(
    election: Election, candidate_actions_map: Optional[dict] = None
) -> dict:
    return {
        "id": election.external_id,
        "title": election.title,
        "created_at": election.created_at.isoformat(),
        "participants": _build_participant_documents_for_election(election),
        "candidates": _build_candidate_documents_for_election(
            election, candidate_actions_map
        ),
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


def build_candidate_document(candidate: Candidate, actions: Optional[dict]) -> dict:
    return {
        "id": str(candidate.id),
        "actions": actions,
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


def _build_candidate_documents_for_election(
    election: Election, candidate_actions_map: Optional[dict] = None
) -> List[dict]:
    candidate_documents = []

    for candidate in election.candidates.all():
        actions = (
            candidate_actions_map.get(candidate.id) if candidate_actions_map else None
        )
        candidate_document = build_candidate_document(candidate, actions)
        candidate_documents.append(candidate_document)

    return candidate_documents

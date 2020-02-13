from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from whatshouldwewatch.movies.models import Movie


class Election(models.Model):
    external_id = models.CharField(unique=True, db_index=True, max_length=255)
    description = models.CharField(max_length=255)
    initiator_id = models.PositiveIntegerField()
    initiator_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    initiator = GenericForeignKey("initiator_type", "initiator_id")
    closed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "Election: {}".format(self.id)


class Participant(models.Model):
    name = models.CharField(max_length=255)
    election = models.ForeignKey(Election, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "Participant: {}".format(self.id)


class Candidate(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.PROTECT)
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "Candidate: {}".format(self.id)


class Vote(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.PROTECT)
    candidate = models.ForeignKey(Candidate, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "Vote: {}".format(self.id)

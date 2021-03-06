from django.db import models

from whichflix.users.models import Device


class Election(models.Model):
    external_id = models.CharField(unique=True, db_index=True, max_length=255)
    title = models.CharField(max_length=255)
    closed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "Election: {}".format(self.id)


class Participant(models.Model):
    name = models.CharField(max_length=255)
    device = models.ForeignKey(Device, on_delete=models.PROTECT)
    election = models.ForeignKey(
        Election, related_name="participants", on_delete=models.PROTECT
    )
    is_initiator = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["device", "election"]

    def __str__(self) -> str:
        return "Participant: {}".format(self.id)


class Candidate(models.Model):
    participant = models.ForeignKey(
        Participant, related_name="candidates", on_delete=models.PROTECT
    )
    election = models.ForeignKey(
        Election, related_name="candidates", on_delete=models.PROTECT
    )
    movie_id = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["participant", "election", "movie_id"]

    def __str__(self) -> str:
        return "Candidate: {}".format(self.id)


class Vote(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.PROTECT)
    candidate = models.ForeignKey(
        Candidate, related_name="votes", on_delete=models.PROTECT
    )
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["participant", "candidate"]

    def __str__(self) -> str:
        return "Vote: {}".format(self.id)

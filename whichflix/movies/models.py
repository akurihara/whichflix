from django.db import models

from whichflix.movies import constants


class Movie(models.Model):
    provider_slug = models.CharField(
        max_length=255, choices=constants.MOVIE_PROVIDER_CHOICES.items()
    )
    provider_id = models.CharField(max_length=255)

    class Meta:
        unique_together = (("provider_id", "provider_slug"),)
        index_together = (("provider_id", "provider_slug"),)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return "Movie: {}".format(self.id)

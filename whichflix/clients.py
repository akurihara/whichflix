import redis

from whichflix.settings.base import REDIS_AUTH

redis_client = redis.Redis(**REDIS_AUTH)  # type: ignore

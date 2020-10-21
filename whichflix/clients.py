import redis

from whichflix.settings.base import REDIS_URL

redis_client = redis.Redis.from_url(REDIS_URL)  # type: ignore

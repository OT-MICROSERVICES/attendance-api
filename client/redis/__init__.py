"""
Module for client SDK of Redis and respective actions.
- Read particular record
- Read all records
"""
# pylint: disable=import-error
from client.redis.redis_conn import CoreRedisClient

# pylint: disable=too-few-public-methods
class MiddlewareSDKFacade:
    """Class wrapper method for client cache related actions"""
    cache = CoreRedisClient()

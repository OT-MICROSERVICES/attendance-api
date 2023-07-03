"""
Module for client SDK of Postgres and respective actions.
- Creation of record
- Read particular record
- Read all records
- Healthcheck for application
"""
# pylint: disable=import-error
from client.postgres.postgres_conn import CorePostgresClient

# pylint: disable=too-few-public-methods
class DatabaseSDKFacade:
    """Class wrapper method for client db related actions"""
    database = CorePostgresClient()

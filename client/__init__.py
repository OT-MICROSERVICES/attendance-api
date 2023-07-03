"""
Module for client SDK of Postgres and respective actions.
- Creation of record
- Read particular record
- Read all records
- Healthcheck for application
"""
from client.postgres import CorePostgresClient

# pylint: disable=too-few-public-methods
class PostgresSDKFacade:
    """Class wrapper method for client db related actions"""
    database = CorePostgresClient()

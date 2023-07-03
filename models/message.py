"""
Module for defining models of Message used in attendance API
"""

from dataclasses import dataclass

@dataclass
class CustomMessage:
    """Class model for custom message using Flask"""
    message: str

@dataclass
class HealthMessage:
    """Class model for health message using Flask for attendance API"""
    message: str
    postgresql: str
    redis: str
    status: str

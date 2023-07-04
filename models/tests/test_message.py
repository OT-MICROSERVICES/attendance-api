from dataclasses import dataclass
import pytest

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

def test_custom_message():
    # Create an instance of CustomMessage
    custom_message = CustomMessage(message="Hello, World!")

    # Assert that the message attribute is set correctly
    assert custom_message.message == "Hello, World!"

def test_health_message():
    # Create an instance of HealthMessage
    health_message = HealthMessage(message="API is running", postgresql="Connected", redis="Connected", status="OK")

    # Assert that the attributes are set correctly
    assert health_message.message == "API is running"
    assert health_message.postgresql == "Connected"
    assert health_message.redis == "Connected"
    assert health_message.status == "OK"

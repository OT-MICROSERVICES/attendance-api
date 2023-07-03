from dataclasses import dataclass

@dataclass
class CustomMessage:
    message: str

@dataclass
class HealthMessage:
    message: str
    postgresql: str
    redis: str
    status: str

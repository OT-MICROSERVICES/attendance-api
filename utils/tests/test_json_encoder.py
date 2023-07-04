from enum import Enum
from datetime import datetime
from dataclasses import dataclass, asdict, is_dataclass
from json import JSONEncoder
from peewee import Model
from playhouse.shortcuts import model_to_dict
import pytest

@dataclass
class CustomDataClass:
    """Sample dataclass for testing"""
    name: str
    value: int

class SampleEnum(Enum):
    """Sample enum for testing"""
    OPTION1 = 1
    OPTION2 = 2

class SampleModel(Model):
    """Sample model for testing"""
    name = 'sample_model'

class CustomJSONEncoder(JSONEncoder):
    """Class for encoding the different types of JSON objects"""
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        elif isinstance(o, Model):
            return model_to_dict(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, Enum):
            return str(o)
        return super().default(o)

def test_custom_json_encoder_dataclass():
    # Create an instance of a dataclass
    data = CustomDataClass(name="Test", value=123)

    # Initialize the JSON encoder
    encoder = CustomJSONEncoder()

    # Encode the dataclass to JSON
    result = encoder.encode(data)

    # Assert that the result is a JSON string containing the dataclass attributes
    assert result == '{"name": "Test", "value": 123}'

def test_custom_json_encoder_model():
    # Create an instance of a model
    model = SampleModel(name="Sample")

    # Initialize the JSON encoder
    encoder = CustomJSONEncoder()

    # Encode the model to JSON
    result = encoder.encode(model)

    # Assert that the result is a JSON string containing the model attributes
    assert result == '{"id": null}'

def test_custom_json_encoder_datetime():
    # Create a datetime object
    dt = datetime(2023, 7, 1, 12, 0, 0)

    # Initialize the JSON encoder
    encoder = CustomJSONEncoder()

    # Encode the datetime to JSON
    result = encoder.encode(dt)

    # Assert that the result is a JSON string containing the ISO formatted datetime
    assert result == '"2023-07-01T12:00:00"'

def test_custom_json_encoder_enum():
    # Create an enum instance
    enum_value = SampleEnum.OPTION1

    # Initialize the JSON encoder
    encoder = CustomJSONEncoder()

    # Encode the enum to JSON
    result = encoder.encode(enum_value)

    # Assert that the result is a JSON string containing the enum value as a string
    assert result == '"SampleEnum.OPTION1"'

if __name__ == '__main__':
    pytest.main()

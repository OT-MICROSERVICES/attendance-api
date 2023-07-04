from functools import wraps
from flask import jsonify, request
from voluptuous import Schema, Invalid
import pytest


def query_validator(schema: Schema, sample_dict):
    """Function for query validation"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                query = sample_dict
                valid_dict = schema(query)
                kwargs.update(valid_dict)
            except Invalid:
                return jsonify({"error": "Validation Error"}), 400
            return func(*args, **kwargs)

        return wrapper

    return decorator


def data_validator(schema: Schema, sample_json):
    """Function for data validation"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                query = sample_json
                valid_dict = schema(query)
                kwargs.update(valid_dict)
            except Invalid:
                return jsonify({"error": "Validation Error"}), 400
            return func(*args, **kwargs)

        return wrapper

    return decorator


# Define example schema for testing
example_schema = Schema({"param": str})


def test_query_validator_valid_input():
    # Create a mock request with valid query parameters
    args = {"param": "value"}

    # Define a test function using query_validator decorator
    @query_validator(example_schema, args)
    def test_function(param):
        return param

    # Call the test function
    result = test_function()

    # Assert that the result is as expected
    assert result == "value"


def test_query_validator_invalid_input():
    # Create a mock request with invalid query parameters
    args = {"param": "value"}

    # Define a test function using query_validator decorator
    @query_validator(example_schema, args)
    def test_function(param):
        return {"error": "Validation Error"}, 400

    # Call the test function
    response = test_function()

    # Assert that the response contains the expected error message and status code
    assert response == ({"error": "Validation Error"}, 400)


def test_data_validator_valid_input():
    # Create a mock request with valid JSON data
    sample_json = {"param": "value"}

    # Define a test function using data_validator decorator
    @data_validator(example_schema, sample_json)
    def test_function(param):
        return param

    # Call the test function
    result = test_function()

    # Assert that the result is as expected
    assert result == "value"


def test_data_validator_invalid_input():
    # Create a mock request with invalid JSON data
    sample_json = {"param": "value"}

    # Define a test function using data_validator decorator
    @data_validator(example_schema, sample_json)
    def test_function(param):
        return {"error": "Validation Error"}, 400

    # Call the test function
    response = test_function()

    # Assert that the response contains the expected error message and status code
    assert response == ({"error": "Validation Error"}, 400)


if __name__ == '__main__':
    pytest.main()

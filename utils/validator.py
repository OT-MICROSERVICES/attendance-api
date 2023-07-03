from functools import wraps
from flask import jsonify, request
from voluptuous import Schema, Invalid

def query_validator(schema: Schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                query = request.args.to_dict()
                valid_dict = schema(query)
                kwargs.update(valid_dict)
            except Invalid:
                return jsonify({"error": "Validation Error"}), 400
            return func(*args, **kwargs)

        return wrapper

    return decorator


def data_validator(schema: Schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                query = request.get_json()
                valid_dict = schema(query)
                kwargs.update(valid_dict)
            except Invalid as e:
                return jsonify({"error": "Validation Error"}), 400
            return func(*args, **kwargs)

        return wrapper

    return decorator

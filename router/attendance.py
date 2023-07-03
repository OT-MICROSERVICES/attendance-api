"""
Module for all the application routes and their respective handlers
- create_record
- read_record
- read_all_record
- get_detail_healthcheck
- get_healthcheck
"""

# pylint: disable=import-error,invalid-name,redefined-builtin
from flask import Blueprint, jsonify, request
from voluptuous import Schema, Required
from client.postgres import DatabaseSDKFacade
from utils.validator import data_validator
from router.cache import cache

route = Blueprint("attendance", __name__)

@route.route("/attendance/create", methods=["POST"])
@data_validator(
    Schema(
        {
            Required("id"): str,
            Required("name"): str,
            Required("status"): str,
            Required("date"):str,
        }
    )
)
def create_record(
        id: str,
        name: str,
        status: str,
        date: str,
):
    """Function for creating the record in the database"""
    record = DatabaseSDKFacade.database.create_employee_attendance(id, name, status, date)
    return jsonify(record)

@route.route("/attendance/search", methods=["GET"])
@cache.cached(timeout=20)
def read_record():
    """Function for reading the record from the database"""
    args = request.args
    id = args.get("id", default="", type=str)
    if id != "":
        record = DatabaseSDKFacade.database.read_employee_attendance(id)
        return jsonify(record)
    return jsonify({"message": f"Unable to process request, please check query params {id}"}), 400

@route.route("/attendance/search/all", methods=["GET"])
@cache.cached(timeout=20)
def read_all_record():
    """Function for reading all the record from the database"""
    record = DatabaseSDKFacade.database.read_all_employee_attendance()
    return jsonify(record)

@route.route("/attendance/health/detail", methods=["GET"])
def get_detail_healthcheck():
    """Function for getting detailed healthcheck of application"""
    status, status_code = DatabaseSDKFacade.database.attendance_detail_health()
    return jsonify(status), status_code

@route.route("/attendance/health", methods=["GET"])
def get_healthcheck():
    """Function for getting healthcheck of application"""
    status, status_code = DatabaseSDKFacade.database.attendance_health()
    return jsonify(status), status_code

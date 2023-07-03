from flask import Blueprint, jsonify, request
from client import PostgresSDKFacade
from utils.validator import data_validator
from voluptuous import Schema, Required

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
    record = PostgresSDKFacade.database.create_employee_attendance(id, name, status, date)
    return jsonify(record)

@route.route("/attendance/search", methods=["GET"])
def read_record():
    args = request.args
    id = args.get("id", default="", type=str)
    if id != "":
        record = PostgresSDKFacade.database.read_employee_attendance(id)
        return jsonify(record)
    return jsonify({"message": f"Unable to process request, please check query params {id}"}), 400

@route.route("/attendance/search/all", methods=["GET"])
def read_all_record():
    record = PostgresSDKFacade.database.read_all_employee_attendance()
    return jsonify(record)

@route.route("/attendance/health", methods=["GET"])
def get_healthcheck():
    status, status_code = PostgresSDKFacade.database.attendance_health()
    return jsonify(status), status_code

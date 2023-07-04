"""
Module for all the application routes and their respective handlers
- create_record
- read_record
- read_all_record
- get_detail_healthcheck
- get_healthcheck
"""

# pylint: disable=import-error,invalid-name,redefined-builtin
from flask import Blueprint, jsonify, request, route
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
    """
    Function for creating the record in the database
    ---
    consumes:
      - application/json
    description: Create record of employee attendance
    produces:
      - application/json
    parameters:
    - description: Attendance Data Payload
      in: body
      name: attendance
      required: true
      schema:
        $ref: '#/definitions/EmployeeInfo'
    definitions:
      EmployeeInfo:
        properties:
          id:
            type: string
          name:
            type: string
          status:
            type: string
          date:
            type: string
        type: object
    responses:
      200:
        description: OK
        schema:
          $ref: '#/definitions/EmployeeInfo'
    summary: CreateRecord API is for creating particular attendance record
    tags:
      - attendance
    """
    record = DatabaseSDKFacade.database.create_employee_attendance(id, name, status, date)
    return jsonify(record)

@route.route("/attendance/search", methods=["GET"])
@cache.cached(timeout=20)
def read_record():
    """
    Function for reading the record from the database
    ---
    consumes:
      - application/json
    description: Read record of employee attendance
    produces:
      - application/json
    parameters:
    - description: User ID
      in: query
      name: id
      required: true
      type: string
    definitions:
      EmployeeInfo:
        properties:
          id:
            type: string
          name:
            type: string
          status:
            type: string
          date:
            type: string
        type: object
    responses:
      200:
        description: OK
        schema:
          $ref: '#/definitions/EmployeeInfo'
    summary: ReadRecord API is for getting particular attendance record
    tags:
      - attendance
    """
    args = request.args
    id = args.get("id", default="", type=str)
    if id != "":
        record = DatabaseSDKFacade.database.read_employee_attendance(id)
        return jsonify(record)
    return jsonify({"message": f"Unable to process request, please check query params {id}"}), 400

@route.route("/attendance/search/all", methods=["GET"])
@cache.cached(timeout=20)
def read_all_record():
    """
    Function for reading all the record from the database
    ---
    consumes:
      - application/json
    description: Read record of all employee attendance records
    produces:
      - application/json
    definitions:
      EmployeeInfo:
        properties:
          id:
            type: string
          name:
            type: string
          status:
            type: string
          date:
            type: string
        type: object
    responses:
      200:
        description: OK
        schema:
          $ref: '#/definitions/EmployeeInfo'
          type: array
    summary: ReadRecord API is for getting all attendance record
    tags:
      - attendance
    """
    record = DatabaseSDKFacade.database.read_all_employee_attendance()
    return jsonify(record)

@route.route("/attendance/health/detail", methods=["GET"])
def get_detail_healthcheck():
    """
    Function for getting detailed healthcheck of application
    ---
    consumes:
      - application/json
    description: Do detail healthcheck for attendance API
    produces:
      - application/json
    definitions:
      HealthMessage:
        properties:
          message:
            type: string
          postgresql:
            type: string
          redis:
            type: string
          status:
            type: string
        type: object
    responses:
      200:
        description: OK
        schema:
          $ref: '#/definitions/HealthMessage'
    summary: DetailedHealthCheckAPI is a method to perform detailed healthcheck
    tags:
      - healthcheck
    """
    status, status_code = DatabaseSDKFacade.database.attendance_detail_health()
    return jsonify(status), status_code

@route.route("/attendance/health", methods=["GET"])
def get_healthcheck():
    """
    Function for getting healthcheck of application
    ---
    consumes:
      - application/json
    description: Do healthcheck for attendance API
    produces:
      - application/json
    definitions:
      CustomMessage:
        properties:
          message:
            type: string
        type: object
    responses:
      200:
        description: OK
        schema:
          $ref: '#/definitions/CustomMessage'
    summary: HealthCheckAPI is a method to perform healthcheck of application
    tags:
      - healthcheck
    """
    status, status_code = DatabaseSDKFacade.database.attendance_health()
    return jsonify(status), status_code

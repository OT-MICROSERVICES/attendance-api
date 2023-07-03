"""
Module for postgres related methods and class
"""
import os
from collections import OrderedDict
from typing import List
import yaml
import psycopg2
import redis
from models.message import CustomMessage, HealthMessage
from models.user_info import EmployeeInfo

CONFIG_FILE = os.getenv('CONFIG_FILE', 'config.yaml')

def redis_status():
    """Function for getting the health of redis"""
    try:
        with open(CONFIG_FILE, 'r', encoding="utf-8") as config_file:
            yaml_values = yaml.load(config_file, Loader=yaml.FullLoader)
        redis_client = redis.Redis(host=yaml_values['redis']['host'],
                                   port=yaml_values['redis']['port'],
                                   password=yaml_values['redis']['password'],
                                   decode_responses=True)
        redis_client.ping()
        return "up"
    except redis.ConnectionError:
        return "down"


class CorePostgresClient:
    """Class for defining the interface for Postgres Client"""
    def __init__(self):
        with open(CONFIG_FILE, 'r', encoding="utf-8") as config_file:
            yaml_values = yaml.load(config_file, Loader=yaml.FullLoader)
        self.client = psycopg2.connect(database=yaml_values['postgres']['database'],
                                       host=yaml_values['postgres']['host'],
                                       user=yaml_values['postgres']['user'],
                                       password=yaml_values['postgres']['password'],
                                       port=yaml_values['postgres']['port'])

    def _record_to_domain_model(self, response):
        return EmployeeInfo(
            id=response.get("id"),
            name=response.get("name"),
            status=response.get("status"),
            date=response.get("date")
        )

    def read_employee_attendance(self, id_value) -> EmployeeInfo:
        """Function to read a particular employee attendance details"""
        cursor = self.client.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        read_query = f"SELECT id, name, status, date FROM records WHERE id='{id_value}'"
        cursor.execute(read_query)
        response = cursor.fetchone()
        return self._record_to_domain_model(OrderedDict(response))

    def read_all_employee_attendance(self) -> List[EmployeeInfo]:
        """Function to read all employee attendance records"""
        cursor = self.client.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT id, name, status, date FROM records ORDER BY id DESC")
        return list(
            map(
                lambda _: self._record_to_domain_model(_),
                cursor.fetchall(),
            )
        )[::-1]

    # pylint: disable=invalid-name,redefined-builtin
    def create_employee_attendance(self, id, name, status, date):
        """Function to create attendance record of the employee"""
        insert_query = """INSERT INTO records (id, name, status, date) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (id, name, status, date)
        cursor = self.client.cursor()
        cursor.execute(insert_query, record_to_insert)
        self.client.commit()
        return CustomMessage(
            message=f"Successfully created the record for the employee id: ${id}"
        )

    def attendance_detail_health(self):
        """Function to get the detailed health of attendance API"""
        try:
            cursor = self.client.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT id, name, status, date FROM records LIMIT 1")
            return HealthMessage(
                message="Attendance API is running fine and ready to serve requests",
                postgresql="up",
                redis=redis_status(),
                status="up",
            ), 200
        except psycopg2.OperationalError:
            return HealthMessage(
                message="Attendance API is not healthy, please check logs",
                postgresql="down",
                redis=redis_status(),
                status="down",
            ), 400

    def attendance_health(self):
        """Function to get the health of attendance API"""
        try:
            cursor = self.client.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute("SELECT id, name, status, date FROM records LIMIT 1")
            return CustomMessage(
                message="Attendance API is running fine and ready to serve requests",
            ), 200
        except psycopg2.OperationalError:
            return CustomMessage(
                message="Attendance API is not healthy, please check logs",
            ), 400

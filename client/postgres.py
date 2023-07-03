import os
import yaml
import psycopg2
import redis
from models.message import CustomMessage, HealthMessage
from models.user_info import EmployeeInfo
from typing import List
from collections import OrderedDict
import psycopg2.extras

CONFIG_FILE = os.getenv('CONFIG_FILE', 'config.yaml')


def redis_status():
    try:
        with open(CONFIG_FILE, 'r', encoding="utf-8") as config_file:
            yaml_values = yaml.load(config_file, Loader=yaml.FullLoader)
        redis_client = redis.Redis(host=yaml_values['redis']['host'],
                                   port=yaml_values['redis']['port'],
                                   password=yaml_values['redis']['password'],
                                   decode_responses=True)
        redis_client.ping()
        return "up"
    except:
        return "down"


class CorePostgresClient:
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
        cursor = self.client.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        read_query = "SELECT id, name, status, date FROM records WHERE id='%s' ORDER BY id DESC" % id_value
        cursor.execute(read_query)
        response = cursor.fetchone()
        return self._record_to_domain_model(OrderedDict(response))

    def read_all_employee_attendance(self) -> List[EmployeeInfo]:
        cursor = self.client.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT id, name, status, date FROM records ORDER BY id DESC")
        return list(
            map(
                lambda _: self._record_to_domain_model(_),
                cursor.fetchall(),
            )
        )[::-1]

    def create_employee_attendance(self, id, name, status, date):
        insert_query = """INSERT INTO records (id, name, status, date) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (id, name, status, date)
        cursor = self.client.cursor()
        cursor.execute(insert_query, record_to_insert)
        self.client.commit()
        return CustomMessage(
            message=f"Successfully created the record for the employee id: ${id}"
        )

    def attendance_health(self):
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
                message="Attendance API is not running in complete healthy state, please check logs",
                postgresql="down",
                redis=redis_status(),
                status="down",
            ), 400

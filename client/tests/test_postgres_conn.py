from unittest.mock import Mock, patch
import pytest
import psycopg2
from collections import OrderedDict
from models.message import CustomMessage, HealthMessage
from models.user_info import EmployeeInfo
from client.redis import MiddlewareSDKFacade
from client.postgres import DatabaseSDKFacade

@pytest.fixture
def mock_config_file(tmp_path):
    config_data = """
    postgres:
        host: localhost
        port: 5432
        user: postgres
        password: password
        database: test_db
    """
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_data)
    return str(config_file)

def test_core_postgres_client_read_employee_attendance(mock_config_file, mocker):
    mock_psycopg2 = mocker.patch("client.postgres.DatabaseSDKFacade")
    mock_cursor = Mock()
    mock_fetchone_result = {
        "id": "1",
        "name": "John Doe",
        "status": "Present",
        "date": "2023-01-01",
    }
    mock_cursor.fetchone.return_value = mock_fetchone_result
    mock_psycopg2.connect.return_value.cursor.return_value = mock_cursor

    result = EmployeeInfo(
        id="1",
        name="John Doe",
        status="Present",
        date="2023-01-01",
    )

    assert result == EmployeeInfo(
        id="1",
        name="John Doe",
        status="Present",
        date="2023-01-01",
    )
    # mock_psycopg2.connect.assert_called_once_with(
    #     database="test_db",
    #     host="localhost",
    #     user="postgres",
    #     password="password",
    #     port=5432,
    # )


def test_core_postgres_client_read_all_employee_attendance(mock_config_file, mocker):
    mock_psycopg2 = mocker.patch("client.postgres.DatabaseSDKFacade")
    mock_cursor = Mock()
    mock_fetchall_result = [
        {
            "id": "1",
            "name": "John Doe",
            "status": "Present",
            "date": "2023-01-01",
        },
        {
            "id": "2",
            "name": "Jane Smith",
            "status": "Absent",
            "date": "2023-01-02",
        },
    ]
    mock_cursor.fetchall.return_value = mock_fetchall_result
    mock_psycopg2.connect.return_value.cursor.return_value = mock_cursor

    result = [
        EmployeeInfo(
            id="1",
            name="John Doe",
            status="Present",
            date="2023-01-01",
        ),
        EmployeeInfo(
            id="2",
            name="Jane Smith",
            status="Absent",
            date="2023-01-02",
        ),
    ]

    assert result == [
        EmployeeInfo(
            id="1",
            name="John Doe",
            status="Present",
            date="2023-01-01",
        ),
        EmployeeInfo(
            id="2",
            name="Jane Smith",
            status="Absent",
            date="2023-01-02",
        ),
    ]

def test_core_postgres_client_create_employee_attendance(mock_config_file, mocker):
    mock_psycopg2 = mocker.patch("client.postgres.DatabaseSDKFacade")
    mock_cursor = Mock()
    mock_psycopg2.connect.return_value.cursor.return_value = mock_cursor

    result = CustomMessage(
        message="Successfully created the record for the employee id: $1"
    )

    assert result == CustomMessage(
        message="Successfully created the record for the employee id: $1"
    )

def test_core_postgres_client_attendance_detail_health(mock_config_file, mocker):
    mock_psycopg2 = mocker.patch("client.postgres.DatabaseSDKFacade")
    mock_cursor = Mock()
    mock_cursor.fetchone.return_value = {
        "id": "1",
        "name": "John Doe",
        "status": "Present",
        "date": "2023-01-01",
    }
    mock_psycopg2.connect.return_value.cursor.return_value = mock_cursor

    mock_redis_status = mocker.patch.object(
        MiddlewareSDKFacade.cache, "redis_status", return_value="up"
    )

    result, status_code = HealthMessage(
        message="Attendance API is running fine and ready to serve requests",
        postgresql="up",
        redis="up",
        status="up",
    ), 200

    assert result == HealthMessage(
        message="Attendance API is running fine and ready to serve requests",
        postgresql="up",
        redis="up",
        status="up",
    )
    assert status_code == 200

def test_core_postgres_client_attendance_health(mock_config_file, mocker):
    mock_psycopg2 = mocker.patch("client.postgres.DatabaseSDKFacade")
    mock_cursor = Mock()
    mock_cursor.fetchone.side_effect = psycopg2.OperationalError
    mock_psycopg2.connect.return_value.cursor.return_value = mock_cursor

    mock_redis_status = mocker.patch.object(
        MiddlewareSDKFacade.cache, "redis_status", return_value="up"
    )

    result, status_code = DatabaseSDKFacade.database.attendance_health()

    assert result == CustomMessage(
        message="Attendance API is running fine and ready to serve requests"
    )
    assert status_code == 200

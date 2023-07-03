from dataclasses import dataclass
import pytest

@dataclass
class EmployeeInfo:
    """Class model for defining the structure for employee's information"""
    id: str
    name: str
    status: str
    date: str

def test_employee_info():
    # Create an instance of EmployeeInfo
    employee = EmployeeInfo(id="123", name="John Doe", status="Active", date="2023-07-01")

    # Assert that the attributes are set correctly
    assert employee.id == "123"
    assert employee.name == "John Doe"
    assert employee.status == "Active"
    assert employee.date == "2023-07-01"

if __name__ == '__main__':
    pytest.main()

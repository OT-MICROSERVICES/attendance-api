"""
Module for defining models of Employee information used in attendance API
"""

from dataclasses import dataclass

# pylint: disable=invalid-name
@dataclass
class EmployeeInfo:
    """Class model for defining the structure for employee's information"""
    id: str
    name: str
    status: str
    date: str

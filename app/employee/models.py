from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base

import enum
from sqlalchemy import Enum


class EmployeeRoleEnum(enum.Enum):
    DEVELOPER = 'developer'
    AUDITOR = 'auditor'
    ADMIN = 'admin'


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(EmployeeRoleEnum), default=EmployeeRoleEnum.DEVELOPER)

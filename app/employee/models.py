from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base
from core.models import CSPEnum, PermissionRolesEnum


import enum
from sqlalchemy import Enum


# class EmployeeRoleEnum(enum.Enum):
#     DEVELOPER = 'developer'
#     AUDITOR = 'auditor'
#     ADMIN = 'admin'


class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)
    password = Column(String, nullable=False)
    email = Column(String, nullable=True)
    role = Column(Enum(PermissionRolesEnum),
                  default=PermissionRolesEnum.DEVELOPER)

    created_by = Column(Integer, ForeignKey('employees.id'))
    admin = relationship("Employee", remote_side=id,
                         backref="created_employee")

    # only for admin and auditor
    iam_id = Column(Integer, ForeignKey('iamdetails.id'))
    iam = relationship("IAMDetails", backref="employee")

    bucket_id = Column(Integer, ForeignKey('buckets.id'))
    bucket = relationship("Bucket", backref="employee")

    # permission_id = Column(Integer, ForeignKey('permissions.id'))
    # permission = relationship("Permission", backref="employee")


class DeveloperFile(Base):
    __tablename__ = 'developerfiles'
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    upaload_to = Column(Enum(CSPEnum))
    signed_url = Column(String)

    created_by = Column(Integer, ForeignKey('employees.id'))
    developers = relationship("Employee", backref="files")

    bucket_id = Column(Integer, ForeignKey('buckets.id'))
    bucket = relationship("Bucket", backref="developer_files")

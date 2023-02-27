from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base

import enum
from sqlalchemy import Enum
# from sqlalchemy.dialects.sqlite import ARRAY
from sqlalchemy.dialects.postgresql import ARRAY

from core.constants import Constants


class PermissionRolesEnum(enum.Enum):
    DEVELOPER = 'developer'
    AUDITOR = 'auditor'
    ADMIN = 'admin'
    COMPANY = 'company'


class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, index=True)
    role = Column(Enum(PermissionRolesEnum), unique=True)
    type = Column(String, nullable=True)
    permissions = Column(ARRAY(String))
    # default=[Constants.PUT_OBJECT, Constants.GET_OBJECT]


class CSPEnum(enum.Enum):
    AWS = 'aws'
    GCP = 'gcp'
    OTHER = 'other'


class IAMDetails(Base):
    __tablename__ = 'iamdetails'
    id = Column(Integer, primary_key=True, index=True)
    role = Column(Enum(PermissionRolesEnum))
    iam_username = Column(String, unique=True)
    iam_csp = Column(Enum(CSPEnum))
    accesskey = Column(String)
    secretkey = Column(String)
    permissions = Column(ARRAY(String))


class Bucket(Base):
    __tablename__ = 'buckets'
    id = Column(Integer, primary_key=True, index=True)
    bucket_name = Column(String, unique=True)
    csp = Column(Enum(CSPEnum))
    comment = Column(String, nullable=True)
    role_type = Column(Enum(PermissionRolesEnum),
                       default=PermissionRolesEnum.DEVELOPER)

    iam_id = Column(Integer, ForeignKey('iamdetails.id'))  # bucket owner
    owner = relationship("IAMDetails", backref="buckets")


class Object(Base):
    __tablename__ = 'objects'
    id = Column(Integer, primary_key=True, index=True)
    object_name = Column(String)
    signed_url = Column(String)

    bucket_id = Column(Integer, ForeignKey('buckets.id'))
    bucket = relationship("Bucket", backref="objects")

    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee_owner = relationship("Employee",
                                  backref="objects")

    company_id = Column(Integer, ForeignKey('companies.id'))
    company_owner = relationship("Company", backref="objects")

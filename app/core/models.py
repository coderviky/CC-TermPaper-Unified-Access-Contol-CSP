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
    role = Column(Enum(PermissionRolesEnum))
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
    iam_user = Column(String)
    accesskey = Column(String)
    permissions = Column(ARRAY(String))


class Bucket(Base):
    __tablename__ = 'buckets'
    id = Column(Integer, primary_key=True, index=True)
    bucket_id = Column(String)
    bucket_csp = Column(Enum(CSPEnum))
    comment = Column(String, nullable=True)
    bucket_type = Column(Enum(PermissionRolesEnum),
                         default=PermissionRolesEnum.DEVELOPER)

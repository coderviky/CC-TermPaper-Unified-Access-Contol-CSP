from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base

import enum
from sqlalchemy import Enum
# from sqlalchemy.dialects.sqlite import ARRAY
from sqlalchemy.dialects.postgresql import ARRAY

from core.constants import Constants


####### ------- ABAC ------- #######

## -- Enums -- ##
# user attributes enums
class UserRolesEnum(enum.Enum):
    '''role'''
    DEVELOPER = 'developer'
    AUDITOR = 'auditor'
    ADMIN = 'admin'
    COMPANY = 'company'


# object attributes enums
# Type  - values {bucket, bucket_policy, file}
class ObjectTypeEnum(enum.Enum):
    '''type'''
    BUCKET = 'bucket'
    BUCKETPOLICY = 'bucket_policy'
    FILE = 'file'


# environment attributes enums
# Day  -  values {weekday, weekend}
class EnvDayEnum(enum.Enum):
    '''day'''
    WEEKDAY = 'weekday'
    WEEKEND = 'weekend'


# operation enums
# {create, get, list, delete}
class OperationEnum(enum.Enum):
    '''operation'''
    CREATE = 'create'
    GET = 'get'
    LIST = 'list'
    DELETE = 'delete'


# # inherited enums with any
# class UserRolesEnumAny(UserRolesEnum):
#     ANY = 'any'


# class ObjectTypeEnumAny(ObjectTypeEnum):
#     ANY = 'any'


# class EnvDayEnumAny(EnvDayEnum):
#     ANY = 'any'


## -- Tables -- ##
# object table - attributes as column and values as
# OR
# Policy table - object attributes and env attributes as column & operations as column
# User_Role & values: {admin, auditor, developer, company, any}
# Object_Type & values {bucket, bucket_policy, file, any}
# Env_Day & values {weekday, weekend, any}
# Operation & values {create, get, list, delete, any}
class PolicyRule(Base):
    __tablename__ = 'policy_rules'
    id = Column(Integer, primary_key=True, index=True)
    user_role = Column(Enum(UserRolesEnum))
    object_type = Column(Enum(ObjectTypeEnum))
    env_day = Column(Enum(EnvDayEnum))
    operation = Column(Enum(OperationEnum))
    description = Column(String, nullable=True)


# class PolicyRule(Base):
#     __tablename__ = 'policy_rules'
#     id = Column(Integer, primary_key=True, index=True)
#     user_role = Column(Enum(UserRolesEnumAny), default=UserRolesEnumAny.ANY)
#     object_type = Column(Enum(ObjectTypeEnumAny),
#                          default=ObjectTypeEnumAny.ANY)
#     env_day = Column(Enum(EnvDayEnumAny), default=EnvDayEnumAny.ANY)
#     operation = Column(Enum(OperationEnum), nullable=False)
#     description = Column(String, nullable=True)


# when app will start -> generate poltree using data from Policy table
# whenever request is made -> create request_tuple -> evaluate request_tuple using poltree


class CSPEnum(enum.Enum):
    AWS = 'aws'
    GCP = 'gcp'
    OTHER = 'other'


class IAMDetails(Base):
    __tablename__ = 'iamdetails'
    id = Column(Integer, primary_key=True, index=True)
    role = Column(Enum(UserRolesEnum))
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
    role_type = Column(Enum(UserRolesEnum),
                       default=UserRolesEnum.DEVELOPER)

    iam_id = Column(Integer, ForeignKey('iamdetails.id'))  # bucket owner
    owner = relationship("IAMDetails", backref="buckets")


class BucketObject(Base):
    __tablename__ = 'bucketobjects'
    id = Column(Integer, primary_key=True, index=True)
    object_name = Column(String, unique=True)
    # signed_url = Column(String)

    bucket_id = Column(Integer, ForeignKey('buckets.id'))
    bucket = relationship("Bucket", backref="bucket_objects")

    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee_owner = relationship("Employee",
                                  backref="bucket_objects")

    company_id = Column(Integer, ForeignKey('companies.id'))
    company_owner = relationship("Company", backref="bucket_objects")


##### ------ RBAC
class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, index=True)
    role = Column(Enum(UserRolesEnum), unique=True)
    type = Column(String, nullable=True)
    permissions = Column(ARRAY(String))
    # default=[Constants.PUT_OBJECT, Constants.GET_OBJECT]

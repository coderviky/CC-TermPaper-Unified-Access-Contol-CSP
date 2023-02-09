from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base

import enum
from sqlalchemy import Enum
from sqlalchemy.dialects.sqlite import ARRAY

from core.constants import Constants


class RolesEnum(enum.Enum):
    DEVELOPER = 'developer'
    AUDITOR = 'auditor'
    ADMIN = 'admin'
    COMPANY = 'company'


class Permissions(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, index=True)
    role = Column(Enum(RolesEnum))
    type = Column(String, nullable=True)
    permissions = Column(ARRAY(String))
    # default=[Constants.PUT_OBJECT, Constants.GET_OBJECT]

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base
from core.models import CSPEnum, PermissionRolesEnum

import enum
from sqlalchemy import Enum


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, index=True)
    comapny_name = Column(String)
    username = Column(String)
    email = Column(String, nullable=True)
    password = Column(String, nullable=False)
    role = Column(Enum(PermissionRolesEnum),
                  default=PermissionRolesEnum.COMPANY)

    created_by = Column(Integer, ForeignKey('employees.id'))
    admin = relationship("Employee", backref="created_companies")

    iam_id = Column(Integer, ForeignKey('iamdetails.id'))
    iam = relationship("IAMDetails", backref="company")

    bucket_id = Column(Integer, ForeignKey('buckets.id'))
    bucket = relationship("Bucket", backref="company")

    # permission_id = Column(Integer, ForeignKey('permissions.id'))
    # permission = relationship("Permission", backref="company")


class CompanyFile(Base):
    __tablename__ = 'companyfiles'
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    upaload_to = Column(Enum(CSPEnum))
    signed_url = Column(String)

    created_by = Column(Integer, ForeignKey('companies.id'))
    companies = relationship("Company", backref="files")

    bucket_id = Column(Integer, ForeignKey('buckets.id'))
    bucket = relationship("Bucket", backref="company_files")

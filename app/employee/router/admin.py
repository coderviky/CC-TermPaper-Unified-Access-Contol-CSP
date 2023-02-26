from employee.models import Employee
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, File, Form, UploadFile
from typing import List, Optional
from pydantic import BaseModel

# s3
from csp import aws_s3
from csp import aws_iam

from employee.models import Employee
from core.models import Permission, IAMDetails, PermissionRolesEnum, Bucket, CSPEnum
# from modules.bucket import Bucket, BucketTypeEnum
from company.models import Company

from core import database
get_db = database.get_db


router = APIRouter(prefix="/admin", tags=['admin'])


class CreateDeveloper(BaseModel):
    username: str
    password: str
    name: str
    developer_username: str
    developer_password: str


class CreateAuditor(BaseModel):
    username: str
    password: str
    comapny_name: str
    auditor_username: str
    auditor_password: str


class CreateCompany(BaseModel):
    username: str
    password: str
    comapny_name: str
    company_username: str
    company_password: str


@router.post("/create-developer")
def create_developer(request: CreateDeveloper, db: Session = Depends(get_db)):
    # Return user
    admin = db.query(Employee).filter(Employee.username == request.username,
                                      Employee.password == request.password, Employee.role == PermissionRolesEnum.ADMIN).first()
    if admin is None:
        raise HTTPException(status_code=404, detail="no admin found!")

    # assign bucket
    bucket = db.query(Bucket).filter(
        Bucket.type == PermissionRolesEnum.DEVELOPER).first()

    # create iam and access key
    # iam_details=  aws_iam.create_iam_employee_user(
    #     employee_type=PermissionRolesEnum.DEVELOPER, username, name)
    iam = IAMDetails(role=PermissionRolesEnum.DEVELOPER, iam_user='iam_dev_' +
                     request.username, accesskey='iam_dev_key_'+request.password)
    db.add(iam)
    db.commit()
    db.refresh(iam)

    # create developer account
    developer = Employee(name=request.name, username=request.developer_username,
                         password=request.developer_password, role=PermissionRolesEnum.DEVELOPER, created_by=admin.id, iam_id=iam.id, bucket_id=bucket.id)

    db.add(developer)
    db.commit()
    db.refresh(developer)

    return developer


@router.post("/create-auditor")
def create_auditor(request: CreateAuditor, db: Session = Depends(get_db)):
    # Return user
    admin = db.query(Employee).filter(Employee.username == request.username,
                                      Employee.password == request.password, Employee.role == PermissionRolesEnum.ADMIN).first()
    if admin is None:
        raise HTTPException(status_code=404, detail="no admin found!")

    # create iam
    iam = IAMDetails(role=PermissionRolesEnum.AUDITOR, iam_user='iam_auditor' +
                     request.username, accesskey='iam_auditor_key_'+request.password)
    db.add(iam)
    db.commit()
    db.refresh(iam)

    # create developer account
    auditor = Employee(name=request.name, username=request.auditor_username,
                       password=request.auditor_password, role=PermissionRolesEnum.AUDITOR, created_by=admin.id, iam_id=iam.id)

    db.add(auditor)
    db.commit()
    db.refresh(auditor)

    return auditor


@router.post("/create-company")
def create_company(request: CreateCompany, db: Session = Depends(get_db)):
    # Return user
    admin = db.query(Employee).filter(Employee.username == request.username,
                                      Employee.password == request.password, Employee.role == PermissionRolesEnum.ADMIN).first()
    if admin is None:
        raise HTTPException(status_code=404, detail="no admin found!")

    # create iam
    # iam_details=  aws_iam.create_iam_employee_user(
    #     employee_type=PermissionRolesEnum.DEVELOPER, username, name)
    iam = IAMDetails(role=PermissionRolesEnum.COMPANY, iam_user='iam_comapny' +
                     request.username, accesskey='iam_company_key_'+request.password)
    db.add(iam)
    db.commit()
    db.refresh(iam)

    # create bucket
    # bucket_details=  aws_s3.create_bucket()
    bucket = Bucket(bucket_id='12345', role=PermissionRolesEnum.COMPANY,
                    bucket_csp=CSPEnum.AWS,
                    bucket_type=PermissionRolesEnum.COMPANY)
    db.add(bucket)
    db.commit()
    db.refresh(bucket)

    # create developer account
    company = Company(comapny_name=request.comapny_name, username=request.company_username,
                      password=request.company_password, role=PermissionRolesEnum.COMPANY, created_by=admin.id, iam_id=iam.id, bucket_id=bucket.id)

    db.add(company)
    db.commit()
    db.refresh(company)

    return company

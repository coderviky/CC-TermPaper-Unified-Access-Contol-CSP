
from core.poltree.poltree import generate_data_and_poltree_generation
from employee.models import Employee
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, File, Form, UploadFile
from typing import List, Optional
from pydantic import BaseModel
from core.constants import Constants
import os
from employee.router import rule

# s3
from csp import aws_s3
from csp import aws_iam

from employee.models import Employee
from core.models import Permission, IAMDetails, UserRolesEnum, Bucket, CSPEnum, PolicyRule, UserRolesEnum, ObjectTypeEnum, EnvDayEnum, OperationEnum
# from modules.bucket import Bucket
from company.models import Company

from core import database
get_db = database.get_db


router = APIRouter(prefix="/admin", tags=['admin'])

router.include_router(rule.router)


class CreateDeveloper(BaseModel):
    username: str
    password: str
    name: str
    developer_username: str
    developer_password: str


@router.post("/create-developer")
def create_developer(request: CreateDeveloper, db: Session = Depends(get_db)):
    # Return user
    admin: Employee = db.query(Employee).filter(Employee.username == request.username,
                                                Employee.password == request.password, Employee.role == UserRolesEnum.ADMIN).first()
    if admin is None:
        raise HTTPException(status_code=404, detail="no admin found!")

    # assign bucket
    bucket: Bucket = db.query(Bucket).filter(
        Bucket.role_type == UserRolesEnum.DEVELOPER).first()

    # # create iam and access key
    # # iam_details=  aws_iam.create_iam_employee_user(
    # #     employee_type=PermissionRolesEnum.DEVELOPER, username, name)
    # iam = IAMDetails(role=PermissionRolesEnum.DEVELOPER, iam_user='iam_dev_' +
    #                  request.username, accesskey='iam_dev_key_'+request.password)
    # db.add(iam)
    # db.commit()
    # db.refresh(iam)

    # create developer account
    developer = Employee(name=request.name, username=request.developer_username,
                         password=request.developer_password, role=UserRolesEnum.DEVELOPER, created_by=admin.id, bucket_id=bucket.id)

    db.add(developer)
    db.commit()
    db.refresh(developer)

    ########## generate poltree everytime whenever new object or user added ##########
    generate_data_and_poltree_generation(db)

    return developer


class CreateAuditor(BaseModel):
    username: str
    password: str
    comapny_name: str
    auditor_username: str
    auditor_password: str


@router.post("/create-auditor")
def create_auditor(request: CreateAuditor, db: Session = Depends(get_db)):
    # Return user
    admin = db.query(Employee).filter(Employee.username == request.username,
                                      Employee.password == request.password, Employee.role == UserRolesEnum.ADMIN).first()
    if admin is None:
        raise HTTPException(status_code=404, detail="no admin found!")

    # create iam
    iam = IAMDetails(role=UserRolesEnum.AUDITOR, iam_user='iam_auditor' +
                     request.username, accesskey='iam_auditor_key_'+request.password)
    db.add(iam)
    db.commit()
    db.refresh(iam)

    # create developer account
    auditor = Employee(name=request.name, username=request.auditor_username,
                       password=request.auditor_password, role=UserRolesEnum.AUDITOR, created_by=admin.id, iam_id=iam.id)

    db.add(auditor)
    db.commit()
    db.refresh(auditor)

    ########## generate poltree everytime whenever new object or user added ##########
    generate_data_and_poltree_generation(db)

    return auditor


class CreateCompany(BaseModel):
    username: str
    password: str
    comapny_name: str
    company_username: str
    company_password: str


@router.post("/create-company")
def create_company(request: CreateCompany, db: Session = Depends(get_db)):
    # Return user
    admin = db.query(Employee).filter(Employee.username == request.username,
                                      Employee.password == request.password, Employee.role == UserRolesEnum.ADMIN).first()
    if admin is None:
        raise HTTPException(status_code=404, detail="no admin found!")

    # create iam
    # iam_details=  aws_iam.create_iam_employee_user(
    #     employee_type=PermissionRolesEnum.DEVELOPER, username, name)
    iam = IAMDetails(role=UserRolesEnum.COMPANY, iam_user='iam_comapny' +
                     request.username, accesskey='iam_company_key_'+request.password)
    db.add(iam)
    db.commit()
    db.refresh(iam)

    # create bucket
    # bucket_details=  aws_s3.create_bucket()
    bucket = Bucket(bucket_id='12345', role=UserRolesEnum.COMPANY,
                    bucket_csp=CSPEnum.AWS,
                    bucket_type=UserRolesEnum.COMPANY)
    db.add(bucket)
    db.commit()
    db.refresh(bucket)

    # create developer account
    company = Company(comapny_name=request.comapny_name, username=request.company_username,
                      password=request.company_password, role=UserRolesEnum.COMPANY, created_by=admin.id, iam_id=iam.id, bucket_id=bucket.id)

    db.add(company)
    db.commit()
    db.refresh(company)

    ########## generate poltree everytime whenever new object or user added ##########
    generate_data_and_poltree_generation(db)

    return company


class InitData(BaseModel):
    passkey: str
    # create admin
    admin_username: str
    admin_password: str

    # create iam user for admin
    iam_username: str
    iam_csp: CSPEnum = CSPEnum.AWS
    iam_accesskey: str
    iam_secretkey: str

    # create developer bucket
    developer_bucket_name: str
    developer_bucket_csp: CSPEnum = CSPEnum.AWS

    # get rules data
    rules_data: List[rule.CreateRule]

# init db with admin username password aws iam detail


@router.post("/init-data")
def init(request: InitData, db: Session = Depends(get_db)):
    # check passkey from env
    if request.passkey != os.environ['PASSKEY']:
        raise HTTPException(status_code=401, detail="passkey not matched!")

    # create iam user for admin
    admin_iam = IAMDetails(role=UserRolesEnum.ADMIN,
                           iam_username=request.iam_username, iam_csp=request.iam_csp,
                           accesskey=request.iam_accesskey,
                           secretkey=request.iam_secretkey,
                           )

    db.add(admin_iam)
    db.commit()
    db.refresh(admin_iam)

    admin = Employee(name='Admin', username=request.admin_username,
                     password=request.admin_password, role=UserRolesEnum.ADMIN, iam_id=admin_iam.id)
    db.add(admin)

    ####### ------- ABAC ------- #######
    ## -- add policies in db -- ##
    for req_rule in request.rules_data:
        db_rule = PolicyRule(
            user_role=req_rule.user_role,
            object_type=req_rule.object_type,
            env_day=req_rule.env_day,
            operation=req_rule.operation,
            description=req_rule.description,
        )
        db.add(db_rule)

    db.commit()
    # get all rules
    all_rules = db.query(PolicyRule).all()

    ## -- Genrate PolTree -- ##
    # get data from db
    # generate pol tree -> store in variable (in poltree.py)

    ####### ------- ABAC END ------- #######

    # ---- RBAC ----
    # create permissions direct
    # # admin
    admin_permission_list = [
        Constants.CREATE_BUCKET_POLICY,
        Constants.CREATE_BUCKET,
        Constants.GET_LIST_OF_ALL_BUCKETS,
        Constants.GET_BUCKET_POLICY,
        Constants.CREATE_DEVELOPER_USER,
        Constants.CREATE_AUDITOR_USER,
        Constants.CREATE_COMPANY_CUSTOMER]
    admin_permission = Permission(
        role=UserRolesEnum.ADMIN, permissions=admin_permission_list)

    # #auditor
    auditor_permission = Permission(
        role=UserRolesEnum.AUDITOR, permissions=[
            Constants.GET_BUCKET_POLICY, Constants.GET_LIST_OF_ALL_BUCKETS]
    )

    # #developer
    developer_permission = Permission(
        role=UserRolesEnum.DEVELOPER, permissions=[Constants.GET_SIGNED_URL])

    # #company
    company_permission = Permission(
        role=UserRolesEnum.COMPANY, permissions=[Constants.GET_SIGNED_URL, Constants.GET_LIST_OF_ALL_FILES, Constants.DELETE_FILE_BY_ID])

    db.add_all([admin_permission, auditor_permission,
                developer_permission, company_permission])
    db.commit()

    # ---- RBAC End ----

    # create developer bucket
    developer_bucket = Bucket(bucket_name=request.developer_bucket_name,
                              csp=request.developer_bucket_csp, iam_id=admin_iam.id, role_type=UserRolesEnum.DEVELOPER)
    db.add(developer_bucket)

    db.commit()
    db.refresh(admin)
    db.refresh(admin_permission)
    db.refresh(auditor_permission)
    db.refresh(developer_permission)
    db.refresh(company_permission)
    db.refresh(developer_bucket)

    ########## generate poltree everytime whenever new object or user added ##########
    generate_data_and_poltree_generation(db)

    return {"admin": admin, "admin_iam": admin_iam, "permissions": [
        admin_permission, auditor_permission, developer_permission, company_permission
    ], "developer_bucket": developer_bucket, "rules": all_rules}


from employee.models import Employee
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, File, Form, UploadFile
from typing import List, Optional
from pydantic import BaseModel
from core.constants import Constants
import os

# s3
from csp import aws_s3
from csp import aws_iam

from employee.models import Employee
from core.models import Permission, IAMDetails, UserRolesEnum, Bucket, CSPEnum, PolicyRule, UserRolesEnum, ObjectTypeEnum, EnvDayEnum, OperationEnum
# from modules.bucket import Bucket, BucketTypeEnum
from company.models import Company

from core import database
get_db = database.get_db


router = APIRouter(prefix="/rule", tags=['policy rules'])


class CreateRule(BaseModel):
    user_role: UserRolesEnum
    object_type: ObjectTypeEnum
    env_day: EnvDayEnum
    operation: OperationEnum
    description: str

    # user_role: Optional[UserRolesEnum] = None
    # object_type: Optional[ObjectTypeEnum] = None
    # env_day: Optional[EnvDayEnum] = None
    # operation: Optional[OperationEnum] = None
    # description: Optional[str] = None

    # user_role: Optional[str] = None
    # object_type: Optional[str] = None
    # env_day: Optional[str] = None
    # operation: Optional[str] = None
    # description: Optional[str] = None


class CreateRuleWithAdmin(CreateRule):
    # get admin
    admin_username: str
    admin_password: str


class AdminData(BaseModel):
    # get admin
    admin_username: str
    admin_password: str


# @router.post("/")
# def create_rule(request: CreateRuleWithAdmin, db: Session = Depends(get_db)):
#     # Return user
#     admin = db.query(Employee).filter(Employee.username == request.admin_username,
#                                       Employee.password == request.admin_password, Employee.role == UserRolesEnum.ADMIN).first()
#     if admin is None:
#         raise HTTPException(status_code=404, detail="no admin found!")

#     # create rule
#     rule = PolicyRule(user_role=request.user_role,
#                       object_type=request.object_type, env_day=request.env_day, operation=request.operation, description=request.description)
#     db.add(rule)
#     db.commit()
#     db.refresh(rule)
#     print(rule)
#     return {}


# @router.get("/all")
# def get_all_rules(request=AdminData, db: Session = Depends(get_db)):
#     # Return user
#     admin = db.query(Employee).filter(Employee.username == request.admin_username,
#                                       Employee.password == request.admin_password, Employee.role == UserRolesEnum.ADMIN).first()
#     if admin is None:
#         raise HTTPException(status_code=404, detail="no admin found!")

#     rules = db.query(PolicyRule).all()
#     return {}

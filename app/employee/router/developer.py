
from core.poltree.poltree_resolve import resolve_access
from employee.models import Employee
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, File, Form, UploadFile
from typing import List, Optional
from pydantic import BaseModel
from core.constants import Constants
from core.poltree.poltree import generate_data_and_poltree_generation

# s3
from csp import aws_s3
from core.models import Permission, IAMDetails, UserRolesEnum, Bucket, CSPEnum, BucketObject, OperationEnum, EnvDayEnum, ObjectTypeEnum, PolicyRule

from core import database
get_db = database.get_db


router = APIRouter(prefix="/developer", tags=['developer'])


class UploadFileRequest(BaseModel):
    username: str
    password: str
    file_name: str
    # file_size: int


@router.post("/get-upload-signed-url")
def get_upload_signed_url(request: UploadFileRequest, db: Session = Depends(get_db)):
    # Return user
    developer: Employee = db.query(Employee).filter(Employee.username == request.username,
                                                    Employee.password == request.password,
                                                    Employee.role == UserRolesEnum.DEVELOPER).first()
    if developer is None:
        raise HTTPException(
            status_code=404, detail=f'developer with {request.username} not found')

    # check permissions : RBAC
    # dev_permissions: Permission = db.query(Permission).filter(
    #     Permission.role == UserRolesEnum.DEVELOPER).first()
    # if Constants.GET_SIGNED_URL not in dev_permissions.permissions:
    #     raise HTTPException(
    #         status_code=403, detail=f'developer {request.username} has not permission {Constants.GET_SIGNED_URL}')

    # -------------------- $$$$$ check access : ABAC $$$$$ ----------------- #
    # get user role
    user_role = developer.role.value
    # user_role = UserRolesEnum.AUDITOR.value
    object_type = ObjectTypeEnum.FILE.value
    env_day = EnvDayEnum.WEEKDAY.value
    operation = OperationEnum.CREATE.value

    access_request = {UserRolesEnum.__doc__: user_role, ObjectTypeEnum.__doc__: object_type,
                      EnvDayEnum.__doc__: env_day,   OperationEnum.__doc__: operation}

    # get access permision from poltree resolve()
    access_decision = resolve_access(access_request)
    if access_decision == 'deny':
        raise HTTPException(
            status_code=403, detail=f'developer {request.username} has not permission to get signed url')

    # return {"message": "access granted"}

    # get developer bucket data
    bucket: Bucket = developer.bucket
    bucket_owner: IAMDetails = bucket.owner

    if bucket is None or bucket.role_type != UserRolesEnum.DEVELOPER:
        raise HTTPException(status_code=403, detail="no bucket found")

    # aws s3 upload url
    expiration = 3600
    response = aws_s3.get_signed_upload_url(
        bucket_name=bucket.bucket_name, object_name=request.file_name, aws_access_key_id=bucket_owner.accesskey, aws_secret_access_key=bucket_owner.secretkey, expiration=expiration)

    # check object in table
    obj = db.query(BucketObject).filter(BucketObject.object_name ==
                                        request.file_name, BucketObject.employee_id == developer.id).first()
    if obj is None:
        # add filename to object table
        obj = BucketObject(object_name=request.file_name,
                           bucket_id=bucket.id, employee_id=developer.id)
        db.add(obj)
        db.commit()

    ######### generate poltree everytime whenever new object or user added ##########
    generate_data_and_poltree_generation(db)

    return {"filename": request.file_name, "signed_upload_url": response['url'], "fields": response['fields'], "expiration": f'{expiration/60} minutes'}


class DownloadFileRequest(BaseModel):
    username: str
    password: str
    file_name: str


@router.post("/get-download-signed-url")
def get_download_signed_url(request: UploadFileRequest, db: Session = Depends(get_db)):
    # Return user
    developer: Employee = db.query(Employee).filter(Employee.username == request.username,
                                                    Employee.password == request.password,
                                                    Employee.role == UserRolesEnum.DEVELOPER).first()
    if developer is None:
        raise HTTPException(
            status_code=404, detail=f'developer with {request.username} not found')

    # check permissions - RBAC
    # dev_permissions: Permission = db.query(Permission).filter(
    #     Permission.role == UserRolesEnum.DEVELOPER).first()
    # if Constants.GET_SIGNED_URL not in dev_permissions.permissions:
    #     raise HTTPException(
    #         status_code=403, detail=f'developer {request.username} has not permission {Constants.GET_SIGNED_URL}')

    # -------------------- $$$$$ check access : ABAC $$$$$ ----------------- #
    # get user role
    user_role = developer.role.value
    object_type = ObjectTypeEnum.FILE.value
    # base on context
    env_day = EnvDayEnum.WEEKDAY.value
    operation = OperationEnum.GET.value

    access_request = {UserRolesEnum.__doc__: user_role, ObjectTypeEnum.__doc__: object_type,
                      EnvDayEnum.__doc__: env_day,   OperationEnum.__doc__: operation}

    # get access permision from poltree resolve()
    access_decision = resolve_access(access_request)
    if access_decision == 'deny':
        raise HTTPException(
            status_code=403, detail=f'developer {request.username} has not permission to get signed url')

    # check object ownership
    obj = db.query(BucketObject).filter(BucketObject.object_name ==
                                        request.file_name, BucketObject.employee_id == developer.id).first()
    if obj is None:
        raise HTTPException(
            status_code=403, detail=f'file {request.file_name} is not found')

    # get developer bucket data
    bucket: Bucket = developer.bucket
    bucket_owner: IAMDetails = bucket.owner

    if bucket is None or bucket.role_type != UserRolesEnum.DEVELOPER:
        raise HTTPException(status_code=403, detail="no bucket found")

    # aws s3
    expiration = 3600
    signed_url = aws_s3.get_signed_download_url(
        bucket_name=bucket.bucket_name, object_name=request.file_name, aws_access_key_id=bucket_owner.accesskey, aws_secret_access_key=bucket_owner.secretkey, expiration=expiration)

    return {"filename": request.file_name, "signed_download_url": signed_url, "expiration": f'{expiration/60} minutes'}

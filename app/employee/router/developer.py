from employee.models import Employee
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, File, Form, UploadFile
from typing import List, Optional
from pydantic import BaseModel
from core.constants import Constants

# s3
from csp import aws_s3
from core.models import Permission, IAMDetails, PermissionRolesEnum, Bucket, CSPEnum, Object

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
                                                    Employee.role == PermissionRolesEnum.DEVELOPER).first()
    if developer is None:
        raise HTTPException(
            status_code=404, detail=f'developer with {request.username} not found')

    # check permissions
    dev_permissions: Permission = db.query(Permission).filter(
        Permission.role == PermissionRolesEnum.DEVELOPER).first()
    if Constants.GET_SIGNED_URL not in dev_permissions.permissions:
        raise HTTPException(
            status_code=403, detail=f'developer {request.username} has not permission {Constants.GET_SIGNED_URL}')

    # get developer bucket data
    bucket: Bucket = developer.bucket
    bucket_owner: IAMDetails = bucket.owner

    if bucket is None or bucket.role_type != PermissionRolesEnum.DEVELOPER:
        raise HTTPException(status_code=403, detail="no bucket found")

    # aws s3 upload url
    expiration = 3600
    response = aws_s3.get_signed_upload_url(
        bucket_name=bucket.bucket_name, object_name=request.file_name, aws_access_key_id=bucket_owner.accesskey, aws_secret_access_key=bucket_owner.secretkey, expiration=expiration)

    # check object in table
    obj = db.query(Object).filter(Object.object_name ==
                                  request.file_name, Object.employee_id == developer.id).first()
    if obj is None:
        # add filename to object table
        obj = Object(object_name=request.file_name,
                     bucket_id=bucket.id, employee_id=developer.id)
        db.add(obj)
        db.commit()

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
                                                    Employee.role == PermissionRolesEnum.DEVELOPER).first()
    if developer is None:
        raise HTTPException(
            status_code=404, detail=f'developer with {request.username} not found')

    # check permissions
    dev_permissions: Permission = db.query(Permission).filter(
        Permission.role == PermissionRolesEnum.DEVELOPER).first()
    if Constants.GET_SIGNED_URL not in dev_permissions.permissions:
        raise HTTPException(
            status_code=403, detail=f'developer {request.username} has not permission {Constants.GET_SIGNED_URL}')

    # check object ownership
    obj = db.query(Object).filter(Object.object_name ==
                                  request.file_name, Object.employee_id == developer.id).first()
    if obj is None:
        raise HTTPException(
            status_code=403, detail=f'file {request.file_name} is not found')

    # get developer bucket data
    bucket: Bucket = developer.bucket
    bucket_owner: IAMDetails = bucket.owner

    if bucket is None or bucket.role_type != PermissionRolesEnum.DEVELOPER:
        raise HTTPException(status_code=403, detail="no bucket found")

    # aws s3
    expiration = 3600
    signed_url = aws_s3.get_signed_download_url(
        bucket_name=bucket.bucket_name, object_name=request.file_name, aws_access_key_id=bucket_owner.accesskey, aws_secret_access_key=bucket_owner.secretkey, expiration=expiration)

    return {"filename": request.file_name, "signed_download_url": signed_url, "expiration": f'{expiration/60} minutes'}

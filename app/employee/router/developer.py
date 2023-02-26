from employee.models import Employee
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, File, Form, UploadFile
from typing import List, Optional
from pydantic import BaseModel

# s3
from csp import aws_s3
from core.models import Permission, IAMDetails, PermissionRolesEnum, Bucket, CSPEnum

from core import database
get_db = database.get_db


router = APIRouter(prefix="/developer", tags=['developer'])


class UploadFileRequest(BaseModel):
    username: str
    password: str
    file_name: str
    file_size: int


class DownloadFileRequest(BaseModel):
    username: str
    password: str
    file_name: str
    # file_size: int


@router.post("/upload-file-url")
def get_upload_sined_url(request: UploadFileRequest, db: Session = Depends(get_db)):
    # Return user
    employee = db.query(Employee).filter(Employee.username == request.username, Employee.password ==
                                         request.password, Employee.role == PermissionRolesEnum.DEVELOPER).first()
    # check permissions

    # get bucket data
    bucket = 'a'

    # get access key data

    # send request to s3
    # aws_s3.get_signed_upload_url(bucket_name=bucket, )

    # return sined url
    return {}

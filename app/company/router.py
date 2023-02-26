from employee.models import Employee, EmployeeRoleEnum
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, File, Form, UploadFile
from typing import List, Optional
from pydantic import BaseModel

from core import database
get_db = database.get_db


router = APIRouter(prefix="/company", tags=['company'])


# S3 : PutObject GetObject ListObjects DeleteObject


@router.get("/list")
def list_users(db: Session = Depends(get_db)):
    # Return all users
    employees = db.query(Employee).all()
    return employees


class CreateEmployee(BaseModel):  #
    name: str
    username: str
    email: str
    password: str
    role: Optional[EmployeeRoleEnum]


@router.post('/create')
def create_employee(request: CreateEmployee, db: Session = Depends(get_db)):
    new_employee = Employee(
        name=request.name, email=request.email, password=request.password, role=request.role, username=request.username)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    # create policy for employee base on role
    return new_employee

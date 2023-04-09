import boto3
from botocore.exceptions import NoCredentialsError
import os
from employee.models import Employee
from core.models import UserRolesEnum


# def create_iam_employee_user(employee_type: PermissionRolesEnum):
#     return 'iam user created and returning iam details'

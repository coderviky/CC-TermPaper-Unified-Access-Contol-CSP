import boto3
from botocore.exceptions import NoCredentialsError
import os
from employee.models import Employee
from core.models import PermissionRolesEnum


def create_iam_employee_user(employee_type: PermissionRolesEnum):
    return 'iam user created and returning iam details'
    # try:
    #     s3 = boto3.client('s3',
    #                       aws_access_key_id=aws_access_key_id,
    #                       aws_secret_access_key=aws_secret_access_key)

    #     presigned_post = s3.generate_presigned_post(
    #         Bucket=bucket_name, Key=file_name)

    #     return presigned_post

    # except NoCredentialsError as e:
    #     print("Credentials not available, please provide AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables")
    #     raise e


def get_download_url(bucket_name, object_name, aws_access_key_id, aws_secret_access_key):
    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)
        response = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": bucket_name,
                "Key": object_name
            },
            ExpiresIn=3600
        )
        return response
    except Exception as e:
        print(e)
        return None

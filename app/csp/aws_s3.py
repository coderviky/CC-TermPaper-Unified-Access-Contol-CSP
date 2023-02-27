import boto3
from botocore.exceptions import NoCredentialsError
import os


def get_signed_upload_url(bucket_name, object_name, aws_access_key_id, aws_secret_access_key, fields=None, conditions=None, expiration=3600):
    """Generate a presigned URL S3 POST request to upload a file

    :param bucket_name: string
    :param object_name: string
    :param fields: Dictionary of prefilled form fields
    :param conditions: List of conditions to include in the policy
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Dictionary with the following keys:
        url: URL to post to
        fields: Dictionary of form fields and values to submit with the POST
    :return: None if error.
    """
    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)

        response = s3.generate_presigned_post(bucket_name,
                                              object_name,
                                              Fields=fields,
                                              Conditions=conditions,
                                              ExpiresIn=expiration)
        print(response)
        return response

    except NoCredentialsError as e:
        print("Credentials not available, please provide AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        raise e


def get_signed_download_url(bucket_name, object_name, aws_access_key_id, aws_secret_access_key, expiration=3600):
    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)
        response = s3.generate_presigned_url(
            'get_object', Params={"Bucket": bucket_name, "Key": object_name}, ExpiresIn=expiration
        )
        return response
    except Exception as e:
        print(e)
        return None


def create_bucket_for_company(company):
    return 'bucket created for compnay'

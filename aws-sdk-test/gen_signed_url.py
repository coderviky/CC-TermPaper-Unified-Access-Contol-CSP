import boto3
from botocore.exceptions import ClientError
import datetime

# Replace with your own access key and secret access key


def get_signed_url(key):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    # Set the desired expiration time for the signed URL (in seconds)
    expiration = 3600

    bucketname = 'csp-test-bucket-0987654321'

    # Generate a presigned URL for the S3 object
    try:
        response = s3.generate_presigned_url('get_object',
                                             Params={
                                                 'Bucket': bucketname, 'Key': key  # filename
                                             },
                                             ExpiresIn=expiration)
        print(response)
        return response
    except ClientError as e:
        raise e
        # print(e)

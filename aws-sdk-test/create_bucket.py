import boto3

# Replace with your own access key and secret access key


# Set up S3 client using access keys
s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                         aws_secret_access_key=SECRET_KEY)

# Replace with your desired bucket name
bucket_name = 'csp-test-bucket-0987654321'


# Create the bucket
response = s3_client.create_bucket(Bucket=bucket_name)

# Print the response
print(response)

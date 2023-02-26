import requests
from gen_signed_url import get_signed_url

# Replace with your pre-signed URL and local file path
# url = "https://csp-test-bucket-0987654321.s3.amazonaws.com/abc?AWSAccessKeyId=AKIAYER34XFCXUMQDAUK&Signature=SEb%2FNaoaueGWixUvkDjHDoKO%2BdQ%3D&Expires=1677414344"

# url = get_signed_url(key='abcd.txt')

url = 'https://csp-test-bucket-0987654321.s3.amazonaws.com/abcd.txt?AWSAccessKeyId=AKIAYER34XFCXUMQDAUK&Signature=mS6C6ImUSMxUJfgv5s0P8ItjJFo%3D&Expires=1677415734'

file_path = "./abcd.txt"

# Read the file into memory
with open(file_path, "rb") as f:
    file_data = f.read()
    print(file_data)

# Upload the file to S3 using the pre-signed URL
response = requests.put(url,
                        # data=file_data
                        files=file_data
                        )

# Check the response status code
if response.status_code == 200:
    print("File uploaded successfully!")
else:
    print(response)
    print("Error uploading file. Status code:", response.status_code)

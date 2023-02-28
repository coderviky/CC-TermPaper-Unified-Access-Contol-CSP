import requests
from globalvariables import baseURL, GlobalVariables


# upload url
def dev_get_upload_signed_url(data):
    response = requests.post(
        f'{baseURL}/developer/get-upload-signed-url', json=data)
    print(response.json())


# download url
def dev_get_download_signed_url(data):
    response = requests.post(
        f'{baseURL}/developer/get-download-signed-url', json=data)
    print(response.json())


def main():
    print("in main")
    # Generate a presigned S3 POST URL
    object_name = 'cms.png'
    data = {
        "username": GlobalVariables.DEV_USERNAME1,
        "password": GlobalVariables.DEV_USERNAME1,
        "file_name": object_name
    }
    response = requests.post(
        f'{baseURL}/developer/get-upload-signed-url', json=data)
    if response is None:
        exit(1)

    res_json = response.json()

    print(res_json)

    # Demonstrate how another Python program can use the presigned URL to upload a file
    with open(object_name, 'rb') as f:
        files = {'file': (object_name, f)}
        http_response = requests.post(
            res_json['signed_upload_url'], data=res_json['fields'], files=files)

    # If successful, returns HTTP status code 204
    print(f'File upload HTTP status code: {http_response.status_code}')


if __name__ == "__main__":
    main()

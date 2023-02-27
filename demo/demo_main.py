from demo_admin import admin_create_developer, admin_create_auditor, admin_create_company, admin_initdata
from demo_developer import dev_get_upload_signed_url, dev_get_download_signed_url
from pydantic import BaseModel
import sys
from globalvariables import GlobalVariables


def create_developer():
    # create developer
    developer_data1 = {
        "username": "admin",
        "password": "admin",
        "name": GlobalVariables.DEV_USERNAME1,
        "developer_username": GlobalVariables.DEV_USERNAME1,
        "developer_password": GlobalVariables.DEV_USERNAME1
    }
    admin_create_developer(data=developer_data1)


def create_auditor():
    # create auditor
    auditor_data1 = {

    }
    admin_create_auditor(data=auditor_data1)


def create_company():
    # create company
    company_data1 = {

    }
    admin_create_company(data=company_data1)


def dev_get_upload_url():
    # developer data
    dev_data = {
        "username": GlobalVariables.DEV_USERNAME1,
        "password": GlobalVariables.DEV_USERNAME1,
        "file_name": "string"
    }
    dev_get_upload_signed_url(data=dev_data)


def dev_get_download_url():
    # developer data
    dev_data = {
        "username": GlobalVariables.DEV_USERNAME1,
        "password": GlobalVariables.DEV_USERNAME1,
        "file_name": "abcd.txt"
    }
    dev_get_download_signed_url(data=dev_data)


def init_data():
    # data
    data = {
        "passkey": "init_data_passkey",
        "admin_username": "admin",
        "admin_password": "admin",

        "iam_username": "viky",
        "iam_csp": "aws",
        "iam_accesskey": "AKIAYER34XFCXUMQDAUK",
        "iam_secretkey": "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",

        "developer_bucket_name": "cfb-developer",
        "developer_bucket_csp": "aws"
    }
    admin_initdata(data)


INFO = """please provide one option from
    -init-data :  to init admin, permissions bucket data
    -create-dev : create developer
    -create-auditor : create auditor
    -create-company : create company
    -dev-get-upload-url : developer get signed url
    -dev-get-download-url : developer get signed url
        """

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == '-init-data':
            init_data()
        elif sys.argv[1] == '-create-dev':
            create_developer()
        elif sys.argv[1] == '-create-auditor':
            create_auditor()
        elif sys.argv[1] == '-create-company':
            create_company()
        elif sys.argv[1] == '-dev-get-upload-url':
            dev_get_upload_url()
        elif sys.argv[1] == '-dev-get-download-url':
            dev_get_download_url()
        else:
            print(INFO)
    else:
        print(INFO)

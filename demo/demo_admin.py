
import requests
from globalvariables import baseURL, GlobalVariables


# initdata
def admin_initdata(data):
    response = requests.post(f'{baseURL}/admin/init-data', json=data)
    print(response.json())
    # if (response.status_code == 200):
    #     print(response.json())
    # elif (response.status_code == 401):
    #     print(response.json())
    # return response


# create Developer
def admin_create_developer(data):
    response = requests.post(f'{baseURL}/admin/create-developer', json=data)
    print(response.json())
    # if (response.status_code == 200):
    #     print(response.json())
    # return response


# create auditor
def admin_create_auditor(data):
    response = requests.post(f'{baseURL}/admin/create-auditor', json=data)
    if (response.status_code == 200):
        print(response.json())
    # return response


# create company
def admin_create_company(data):
    response = requests.post(f'{baseURL}/admin/create-company', json=data)
    if (response.status_code == 200):
        print(response.json())
    # return response

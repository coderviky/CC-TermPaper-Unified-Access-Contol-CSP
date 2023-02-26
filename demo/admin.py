
import requests
from globalvariables import baseURL, GlobalVariables


# create Developer
def create_developer(data):
    response = requests.post(f'{baseURL}/admin/create-developer', json=data)
    if (response.status_code == 200):
        print(response.json())
    # return response


# create auditor
def create_auditor(data):
    response = requests.post(f'{baseURL}/admin/create-auditor', json=data)
    if (response.status_code == 200):
        print(response.json())
    # return response


# create company
def create_company(data):
    response = requests.post(f'{baseURL}/admin/create-company', json=data)
    if (response.status_code == 200):
        print(response.json())
    # return response

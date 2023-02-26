from admin import create_developer, create_auditor, create_company
from pydantic import BaseModel


# # create developer
developer_data1 = {
    "username": "string",  # admin username
    "password": "string",  # admin password
    "name": "string",
    "developer_username": "string",
    "developer_password": "string"
}
create_developer(data=developer_data1)


# create auditor
auditor_data1 = {

}
create_auditor(data=auditor_data1)


# create company
company_data1 = {

}
create_company(data=company_data1)


# ------ developer --------

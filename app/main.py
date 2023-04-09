from fastapi import FastAPI
from core.poltree.poltree import generate_data_and_poltree_generation
from core.database import engine
from core import base, database

from employee.router import admin, developer

base.Base.metadata.create_all(engine)

app = FastAPI(title="CFB")


app.include_router(admin.router)
app.include_router(developer.router)

####### ------- ABAC ------- #######

# get_db = database.get_db

## -- Genearate PolTree -- ##
# generate_data_and_poltree_generation()


@app.get("/")
def index():
    return {"hello"}

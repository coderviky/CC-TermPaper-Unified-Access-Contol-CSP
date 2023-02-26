from fastapi import FastAPI
from core.database import engine
from core import base

from employee.router import admin, developer

base.Base.metadata.create_all(engine)

app = FastAPI(title="CFB")


app.include_router(admin.router)
app.include_router(developer.router)


@app.get("/")
def index():
    return {"hello"}

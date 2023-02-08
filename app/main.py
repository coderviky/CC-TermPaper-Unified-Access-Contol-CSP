from fastapi import FastAPI
from core.database import engine
from core import base

from employee import router_employee

base.Base.metadata.create_all(engine)

app = FastAPI(title="CFB")


app.include_router(router_employee.router)


@app.get("/")
def index():
    return {"hello"}

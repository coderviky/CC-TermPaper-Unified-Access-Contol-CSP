from fastapi import FastAPI
from core.database import engine
from core import base

from employee.router import employee

base.Base.metadata.create_all(engine)

app = FastAPI(title="CFB")


app.include_router(employee.router)


@app.get("/")
def index():
    return {"hello"}

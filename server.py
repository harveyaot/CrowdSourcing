from fastapi import FastAPI
from datamodel import Task

app = FastAPI()

@app.get("/")
async def hello_world():
    return "hello world"

@app.post("/tasks/", response_model=Task, response_model_exclude="repsonse")
async def create_task(task:Task):
    return task
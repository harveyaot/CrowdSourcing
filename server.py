import configparser
import shortuuid

from configparser import ExtendedInterpolation
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from datamodel import ServerContext, TaskPublish, TaskFinish, OperationResponse, Worker, Publisher
from mongo_manager import MongoManager

app = FastAPI()
def initialize(s_ctx: ServerContext): pass

# will be initialized
s_ctx = ServerContext()

#region common check
async def check_publisher(publisher_id:str):
    rslt = s_ctx.mongo_manager.find_docfromcol({"account_id":publisher_id}, s_ctx.publisher_col)
    if rslt:
        return rslt['id']
    return None
#endregion


@app.get("/")
async def hello_world():
    return "hello world"

#region Worker
@app.get("/worker/login", response_model=Worker)
async def worker_login(account_id:str):
    rslt = s_ctx.mongo_manager.find_docfromcol(
        {"account_id":account_id}, s_ctx.worker_col)
    if rslt:
        resp =  Worker(**rslt)
    else:
        raise HTTPException(status_code=400, detail="Account not exists")
    return resp

@app.post("/worker/create", response_model=OperationResponse)
async def worker_create(account_id:str):
    try:
        rslt = s_ctx.mongo_manager.find_docfromcol(
            {"account_id":account_id}, s_ctx.worker_col)
        if not rslt:
            #[TODO] mayhave conflicts. 
            workder_id = shortuuid.ShortUUID().random(length=10)
            worker = Worker(id=workder_id, account_id=account_id)
            rslt2 = s_ctx.mongo_manager.insert_doc2col(
                worker.dict(), s_ctx.worker_col)
            resp = OperationResponse(succeed=rslt2.acknowledged)
    except:
        resp = OperationResponse(succeed=False)
    if rslt:
        raise HTTPException(status_code=400, detail="Account existed")
    return resp

@app.post("/publisher/create", response_model=OperationResponse)
async def publihser_create(account_id:str):
    try:
        rslt = s_ctx.mongo_manager.find_docfromcol(
            {"account_id":account_id}, s_ctx.publisher_col)
        if not rslt:
            #[TODO] mayhave conflicts. 
            publihser_id = shortuuid.ShortUUID().random(length=10)
            publisher = Publisher(id=publihser_id, account_id=account_id)
            rslt2 = s_ctx.mongo_manager.insert_doc2col(
                publisher.dict(), s_ctx.publisher_col)
            resp = OperationResponse(succeed=rslt2.acknowledged)
    except:
        resp = OperationResponse(succeed=False)
    if rslt:
        raise HTTPException(status_code=400, detail="Account existed")
    return resp

#endregion

#region Tasks
# tasks realted apis:
@app.get("/tasks/finish/search", response_model=List[TaskFinish])
async def search_finish_tasks(
    update_time_end: int,
    offset: int = 0,
    count: int = 10,
    update_time_start: int = 0,
    worker_id: Optional[int] = None,
    task_id: Optional[int] = None
):
    q = {
        'update_time':
        {'$gte': update_time_start, '$lt': update_time_end},
    }

    if worker_id:
        q['worker_id'] = worker_id

    if task_id:
        q['task_id'] = task_id

    rslt = s_ctx.mongo_manager.find_docsfromcol(
        q,
        offset,
        count,
        s_ctx.task_finish_col
    )
    if rslt:
        resp = [TaskPublish(**e) for e in rslt]
    else:
        resp = []
    return resp


@app.get("/tasks/publish/search", response_model=List[TaskPublish])
async def search_publish_tasks(
    publish_time_end: int,
    expire_time_end: int,
    min_left_num: int = 0,
    publish_time_start: int = 0,
    expire_time_start: int = 0,
    offset: int = 0,
    count: int = 10,
    publisher_id: Optional[int] = None
):
    q = {
        'publish_time':
        {'$gte': publish_time_start, '$lt': publish_time_end},
            'expire_time':
                {'$gte': expire_time_start, '$lt': expire_time_end},
            'left_num':
                {'$gte': min_left_num}
    }

    if publisher_id:
        q['publsiher_id'] = publisher_id

    rslt = s_ctx.mongo_manager.find_docsfromcol(
        q,
        offset,
        count,
        s_ctx.task_publish_col
    )
    if rslt:
        resp = [TaskPublish(**e) for e in rslt]
    else:
        resp = []
    return resp


@app.get("/tasks/publish", response_model=TaskPublish)
async def get_publish_task(task_id: int):
    rslt = s_ctx.mongo_manager.find_docfromcol(
        {'task_id': task_id}, s_ctx.task_publish_col)
    resp = TaskPublish(**rslt)
    return resp


@app.get("/tasks/finish", response_model=TaskFinish)
async def get_finish_task(task_id: int):
    rslt = s_ctx.mongo_manager.find_docfromcol(
        {'task_id': task_id}, s_ctx.task_finish_col)
    resp = TaskFinish(**rslt)
    return resp


@app.post("/tasks/publish_task", response_model=OperationResponse)
async def publsih_task(task: TaskPublish, valid_publisher = Depends(check_publisher)):
    try:
        if not valid_publisher:
            return OperationResponse(succeed=0, detail="Invalid Publisher")
        task.publisher_id = valid_publisher
        rslt = s_ctx.mongo_manager.insert_doc2col(
            task.dict(), s_ctx.task_publish_col)
        resp = OperationResponse(succeed=rslt.acknowledged)
    except:
        resp = OperationResponse(succeed=0)
    return resp


@app.post("/tasks/finish_task", response_model=OperationResponse)
async def finish_task(task: TaskFinish):
    try:
        rslt = s_ctx.mongo_manager.insert_doc2col(
            task.dict(), s_ctx.task_finish_col)
        resp = OperationResponse(succeed=rslt.acknowledged)
    except:
        resp = OperationResponse(succeed=0)
    return resp
#endregion


def initialize(s_ctx):
    config = configparser.ConfigParser(interpolation=ExtendedInterpolation())
    config.read('config/test.ini')
    mongo_port = config.getint('mongodb', 'port')
    mongo_host = config.get('mongodb', 'host')
    mongo_db = config.get('mongodb', 'db')

    s_ctx.mongo_manager = MongoManager(mongo_host, mongo_port, mongo_db)
    s_ctx.task_publish_col = config['mongodb-col']['task_publish']
    s_ctx.task_finish_col = config['mongodb-col']['task_finish']
    s_ctx.publisher_col = config['mongodb-col']['publisher']
    s_ctx.worker_col = config['mongodb-col']['worker']

initialize(s_ctx)

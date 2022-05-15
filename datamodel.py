from protobuf2pydantic import msg2py
from pydantic import validator, BaseModel
from mongo_manager import MongoManager
from protos.gen.pb_python import crowdsourcing_pb2 
from protos.gen.pb_python.crowdsourcing_pb2 import AnswerType, TextImage


TaskPublish = msg2py(crowdsourcing_pb2.TaskPublish)
TaskFinish = msg2py(crowdsourcing_pb2.TaskFinish)
Worker = msg2py(crowdsourcing_pb2.Worker)
Publisher = msg2py(crowdsourcing_pb2.Publisher)


class ServerContext:
    mongo_manager: MongoManager
    task_publish_col:str
    task_finish_col:str
    worker_col:str
    publihser_col:str

class OperationResponse(BaseModel):
    succeed:bool
    detail:str|None
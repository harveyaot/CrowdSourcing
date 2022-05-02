from protobuf2pydantic import msg2py
from pydantic import validator
from protos.gen.pb_python import task_pb2 

class Task(msg2py(task_pb2.Task)):
    pass
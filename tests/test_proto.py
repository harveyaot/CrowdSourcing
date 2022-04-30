import unittest
import json
from protos.gen.pb_python.task_pb2 import Task
import google.protobuf.json_format as jf

class TestProto(unittest.TestCase):

    def test_build(self):
        from protos.gen.pb_python.task_pb2 import Task
        t = Task(name="haha", id=20, publish_time=123445676)
        self.assertEqual(t.publish_time, 123445676, "Should be 20")

    def test_to_json(self):
        t = Task(name="haha", id=20, publish_time=123445676)
        json_p = jf.MessageToJson(t)
        d = json.loads(json_p)
        self.assertEqual(t.name,d['name'] , "haha")
    
    def test_nested_type(self):
        t = Task(name="haha", id=20, publish_time=123445676, request= Task.Request(question="mingju?"))
        self.assertEqual(t.request.question, "mingju?", "mingju?")

if __name__ == '__main__':
    unittest.main()

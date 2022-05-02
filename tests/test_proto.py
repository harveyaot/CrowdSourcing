import unittest
import json
from protos.gen.pb_python.crowdsourcing_pb2 import TaskPublish, TaskFinish, AnswerType, TextImage
import google.protobuf.json_format as jf

class TestProto(unittest.TestCase):

    def test_build(self):
        t = TaskPublish(name="haha", task_id=21, publish_time=1234456766)
        self.assertEqual(t.publish_time, 1234456766, "Should be 1234456766")

    def test_to_json(self):
        t = TaskPublish(name="haha", task_id=20, publish_time=123445676)
        json_p = jf.MessageToJson(t)
        d = json.loads(json_p)
        self.assertEqual(t.name,d['name'] , "haha")
    
    def test_taskpublish(self):
        questions = [TaskPublish.Question(text_images=[TextImage(text="hhhh"),], expected_answer_type=AnswerType.IMAGE),]
        t = TaskPublish(name="haha", task_id=20, publish_time=123445676, questions=questions)
        self.assertEqual(t.questions[0].text_images[0].text, "hhhh", "hhhh")
        self.assertEqual(t.questions[0].expected_answer_type, 1, 1)
        
    def test_taskfinish(self):
        answers = [TaskFinish.Answer(text_images=[TextImage(text="aaaa")], answer_type=AnswerType.TEXT),
                   TaskFinish.Answer(text_images=[TextImage(text="bbbb")], answer_type=AnswerType.TEXT)
                    ]
        t = TaskFinish(task_id=20,answers=answers)
        self.assertEqual(len(t.answers), 2, "should be 2")
        self.assertEqual(t.answers[1].text_images[0].text, "bbbb", "bbbb")

if __name__ == '__main__':
    unittest.main()

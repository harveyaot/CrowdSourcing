import time
import shortuuid
import requests

from protos.gen.pb_python import crowdsourcing_pb2 
from protos.gen.pb_python.crowdsourcing_pb2 import TaskPublish, TaskFinish, AnswerType, TextImage
from google.protobuf.json_format import MessageToDict, MessageToJson

TASK_NAME = "给诗歌配上合适的图片"
publisher_id = "123"
headers = {"Content-Type":"application/json"}
url = "http://localhost:8081/tasks/publish_task?publisher_id=" + publisher_id


def submit_task(t):
    print(MessageToJson(t, preserving_proto_field_name=True,use_integers_for_enums=True))        
    resp = requests.post(url, data=MessageToJson(t, preserving_proto_field_name=True, use_integers_for_enums=True))
    return resp

def run():
    minjus = [
        "山有木兮木有枝，心悦君兮君不知。",
        "人生若只如初见，何事秋风悲画扇。",
        "十年生死两茫茫，不思量，自难忘。",
        "曾经沧海难为水，除却巫山不是云。",
        "玲珑骰子安红豆，入骨相思知不知。",
        "人生如逆旅，我亦是行人。",
        "只愿君心似我心，定不负相思意。",
        "平生不会相思，才会相思，便害相思。",
        "愿得一心人，白头不相离。"
    ]

    for sent in minjus:
        q = TaskPublish.Question(text_images=[TextImage(text=sent)], expected_answer_type=AnswerType.IMAGE)
        publish_time = int(time.time())
        expire_time = publish_time + 3600 * 24 * 30
        qs = [q]
        task_id = shortuuid.ShortUUID().random(length=10)
        print(task_id)
        t = TaskPublish (
                name = TASK_NAME, 
                task_id = task_id,
                publish_time = publish_time, 
                expire_time = expire_time, 
                questions = qs,
                left_num = 2,
                price = 5
            )
        resp = submit_task(t)
        print(f"Submit task {task_id} with response: {resp.status_code}")
        break

if __name__ == "__main__":
    run()


import unittest
import configparser
import json
#import uuid
import time

import google.protobuf.json_format as jf

from protos.gen.pb_python.crowdsourcing_pb2 import TaskPublish
from pymongo import MongoClient

class TestMongo(unittest.TestCase):
    def setUp(self):
        config = configparser.ConfigParser()
        config.read('config/test.ini')
        port = config.getint('mongodb', 'port')
        host = config.get('mongodb', 'host')
        dbname = config.get('mongodb', 'db')
        self.mongo_client = MongoClient(host=host,port=port)
        self.db = self.mongo_client[dbname]
        self.col = self.db['test']
        

    def test_build(self):
        rand_id = int(time.time())
        t = TaskPublish(name="haha", id=rand_id, publish_time=123445676)
        json_p = jf.MessageToJson(t)
        d = json.loads(json_p)
        self.col.insert_one(d)

        return_d = self.col.find_one({'id':rand_id}, {'name':1})
        print(return_d)
        self.assertEqual(return_d['name'], t.name, f"Should be {t.name}")

        return_d = self.col.find_one({'id':rand_id}, {'publishTime':1})
        print(return_d)
        self.assertEqual(return_d['publishTime'], t.publish_time, f"Should be {t.publish_time}")

        return_d = self.col.find_one({'id':rand_id}, {'request':1})
        self.assertEqual(return_d['request']['question'], t.request.question, f"Should be {t.request.question}")

if __name__ == '__main__':
    unittest.main()
from pymongo import MongoClient
import pymongo

class MongoManager:

    def __init__(self, host, port, db):
        self.mongo_client = MongoClient(host=host,port=port)
        self._db = self.mongo_client[db]
    
    def insert_doc2col(self, doc, col):
        col = self._db[col]
        return col.insert_one(doc)
    
    def find_docfromcol(self, query, col):
        col = self._db[col]
        return col.find_one(query)
    
    def find_docsfromcol(self, query, offset, count, col):
        col = self._db[col]
        return col.find(query).skip(offset).limit(count)
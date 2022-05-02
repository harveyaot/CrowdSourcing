import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client.test


class Manager:

    def __init__(self,host="localhost", port=27017):
        self._client = pymongo.MongoClient(host, port)
        
    def get_collecton(self, db, collection):
        db = self._client.getDb(db)
        collection = db.getCollection(collection)
        return collection
from pymongo import MongoClient
import pymongo


class MongoDBModel(object):
    def __init__(self, db, URI=None):
        self.db = db

        # use mongodb server
        if URI is not None:
            self.client = MongoClient(URI, connect=False, maxPoolSize=2)
        
        # use local mongo database if URI is not exist
        if URI is None:
            self.client = MongoClient()
    
    def getByOne(self, collection:str, query):
        db = self.client[self.db]
        result = db[collection].find_one({}, query)
        return result
    
    def insertByOne(self, collection:str, data:dict):
        """
        Desc: only insert single data.
        Args: 
            - db: database's name. string format.
            - collection : collection's name. string format.
            - data: data which will be inserted. dictionary format.
        """
        db = self.client[self.db]
        db[collection].insert_one(data)

    def updateByOne(self, collection, query:dict, new_values:dict):
        db = self.client[self.db]
        db[collection].update_one(query, new_values)
    
    def deleteByOne(self, collection, field, value):
        query = {field : value}
        db = self.client[self.db]
        db[collection].delete_one(query)
    
    def getToken(self):
        db = self.client[self.db]
        token = db['tokens'].find().sort("_id", pymongo.DESCENDING).limit(1)
        return token[0]
    
    def getAllDocument(self, collection:str, query, include_id=False):
        """
        Get all the data inside a collection.
        Returns all the data inside the collection
        """
        db = self.client[self.db]
        if include_id==False:
            query['_id'] = 0
        if include_id==True:
            query['_id'] = 1
        data = db[collection].find({}, query)
        return data
    
    def checkExistingDoc(self, collection, field, value):
        """
        Check if a document exists in a collection.
        Returns True or False
        """
        db = self.client[self.db]
        result = db[collection].find_one({field: value})
        if result is None:
            return False
        else:
            return True
    
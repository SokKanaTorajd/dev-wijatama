from pymongo import MongoClient


class MongoDBModel(object):
    def __init__(self, db, URI=None):
        self.db = db

        # use mongodb server
        if URI is not None:
            self.client = MongoClient(URI, connect=False, maxPoolSize=2)
        
        # use local mongo database if URI is not exist
        if URI is None:
            self.client = MongoClient()
    
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
    
    def getAllDocByOneField(self, collection:str, field:str, include_id=False):
        """
        Desc: get all the data inside a collection by filtering one field.
        Args: 
            - db: database's name. string format.
            - collection : collection's name. string format.
            - field: field's name in the document. string format.
            - include_id : return document id or not. default False, Boolean format.
        Returns all the data inside the collection
        """
        db = self.client[self.db]
        if include_id==False:
            query = {field:1, '_id':0}
        if include_id==True:
            query = {field:1, '_id':1}
        data = db[collection].find({}, query)
        return data
    
    def checkExistingDoc(self, collection, field, value):
        """
        Desc: check if a document exists in a collection.
        Args: 
            - db: database's name. string format.
            - collection : collection's name. string format.
            - field: field's name in the document. string format.
            - value: the value of the field that you want to look for. 
                Depend on the data you are looking for, whether its string, boolean, integer, float, etc.
        Returns True or False
        """
        db = self.client[self.db]
        result = db[collection].find_one({field: value})
        if result is None:
            return False
        else:
            return True
    
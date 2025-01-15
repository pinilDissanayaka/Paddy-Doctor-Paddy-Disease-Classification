import os
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
import logging

load_dotenv(find_dotenv())
logging.basicConfig(filename="log.log",  level=logging.WARNING)

class Admin(object):
    def __init__(self, app) -> None:
        self._bycrypt=Bcrypt(app=app)
        
        
    @classmethod
    def connectDB(cls, databaseName = 'AgriSage'):
        try:
            client=MongoClient(os.getenv('MONGO_CLIENT'))
            db=client[databaseName]
            connectionStatus=True
        except Exception as e:
            print("Database connection failed!")
            connectionStatus=False
            logging.exception(e)
            
        return client, db, connectionStatus
    
    def getDocumentCount(self, collectionName :str, adminUserFlag = None):
        try:
            client, db, connectionStatus=self.connectDB()
            collection=db[collectionName]
            
            if connectionStatus:
                if adminUserFlag is None:
                    count=collection.count_documents({})
                else:
                    count=collection.count_documents({"adminUserFlag" : adminUserFlag})
            else:
                count=None
        except Exception as e:
            logging.exception(e)
        finally:
            client.close()
        
        return count
    
    
    
    
        
        
    


            
        
    
    
    
import os
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv, find_dotenv
from utils.fieldData import FieldData
from utils.fieldData import addData, getData
import logging


load_dotenv(find_dotenv())
logging.basicConfig(filename="log.log")

class Firebase(object):
    def __init__(self) -> None:
        cred=credentials.Certificate("firbase-SDK.json")
        firebase_admin.initialize_app(cred, {"databaseURL": "https://agrisage-85205-default-rtdb.asia-southeast1.firebasedatabase.app/"})


    def getValues(self, key:str):
        try:
            iotData=db.reference('/').child(key).get()
            addData(data=iotData, deviceID=key)
            iotData=getData(deviceID=key)
            return iotData
        except Exception as e:
            logging.exception(e)
            
        


        

        
    
        
        
            


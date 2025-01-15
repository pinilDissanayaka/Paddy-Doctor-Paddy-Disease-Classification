import os
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
import re
import base64
import logging

load_dotenv(find_dotenv())
logging.basicConfig(filename="log.log", level=logging.WARNING)


class Product(object):
    def __init__(self) -> None:
        pass
               
    @classmethod
    def connectDB(cls, databaseName = 'AgriSage', collectionName='Products'):
        try:
            client=MongoClient(os.getenv('MONGO_CLIENT'))
            db=client[databaseName]
            collection=db[collectionName]
            connectionStatus=True
        except Exception as e:
            logging.exception(e)
            print("Database connection failed!")
            connectionStatus=False
            
        return client, collection, connectionStatus
    
    
    
        
    def addProduct(self, fertilizerName:str, useFor:str, fertilizerType:str, manufacturer:str):
        try:
            client, collection, connectionStatus=Product.connectDB()
            
            if connectionStatus:                
                collection.insert_one({"fertilizerName" : fertilizerName, "useFor" : useFor, "fertilizerType" : fertilizerType, "manufacturer" : manufacturer})
                print("Product successfully added.")
                status=True
            else:
                print("Failed adding product.")
                status=False
        except Exception as e:
            logging.exception(e)
        finally:
            client.close()
            
        return status
    
    def updateProduct(self):
        try:
            client, collection, connectionStatus=Product.connectDB()
        finally:
            client.close()
            
    def showAllProducts(self):
        try:
            client, collection, connectionStatus=Product.connectDB()
            if connectionStatus:
                products=collection.find()
                if products:
                    return products
                else:
                    products=None
                    return products
            else:
                products=None
        except Exception as e:
            logging.exception(e)
        #finally:
            #client.close()
            
        return products
    
    
    def recommendProducts(self, useFor:str):
        try:
            client, collection, connectionStatus=Product.connectDB()
            if connectionStatus:
                recommendedProducts=collection.find({"useFor": useFor})
                if recommendedProducts:
                    return recommendedProducts
                else:
                    recommendedProducts=None
                    return recommendedProducts
            else:
                recommendedProducts=None
        except Exception as e:
            logging.exception(e)
        #finally:
            #client.close()
            
        return recommendedProducts
        
        
            
import os
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from utils.fieldData import FieldData
import re
import logging

load_dotenv(find_dotenv())
logging.basicConfig(filename="log.log", level=logging.WARNING)


fieldData=FieldData()

class User(object):
    def __init__(self, app) -> None:
        self._bycrypt=Bcrypt(app=app)
        
        
    @classmethod
    def connectDB(cls, databaseName = 'AgriSage', collectionName='Users'):
        try:
            client=MongoClient(os.getenv('MONGO_CLIENT'))
            db=client[databaseName]
            collection=db[collectionName]
            connectionStatus=True
            
            return client, collection, connectionStatus
        except Exception as e:
            print("Database connection failed!")
            logging.exception(e)
            connectionStatus=False
            
    
           
    def addUser(self, name:str, phoneNumber:str, userName:str, password:str, adminUserFlag='False'):
        try:
            client, collection, connectionStatus=User.connectDB()
            
            if connectionStatus is True:
                _, user=self.getUserByUserName(userName)
        
                
                if user is None:
                    password=self._bycrypt.generate_password_hash(password).decode('utf-8')
                    
                    collection.insert_one({"name" : name, "phoneNumber" : phoneNumber, "userName" : userName, "password" : password, 'adminUserFlag' : adminUserFlag})
                    print("User successfully added.")
                    status=True
                else:
                    print("Failed adding user.")
                    status=False
                    
            return status
        except Exception as e:
            logging.exception(e)
        finally:
            client.close()
            
    
          
    def getUserByUserName(self, userName : str):
        try:
            client, collection, connectionStatus=User.connectDB()
            if connectionStatus is True:
                user=collection.find_one({"userName" : userName})
                if user is None:
                    status='User not found'
                else:
                    status='User was found'
                    
            return status, user

        except Exception as e:
            logging.exception(e)   
        finally:
            client.close()
            
    
    
    def logInUser(self, userName:str, password:str):
        try:
            client, collection, connectionStatus=User.connectDB()
        
            if connectionStatus is True:
                _, user=self.getUserByUserName(userName)
            
                if user is None:
                    status="User not found"
                    print("User not found")
                else:
                    isValid =self._bycrypt.check_password_hash(user['password'], password)
                    
                    if isValid:
                        print("Login successful")
                        user=user
                        status="Login successful"
                    else:
                        print("Incorrect password")
                        user=None
                        status="Incorrect password"
                        
            return status, user
        except Exception as e:
            logging.exception(e)
        finally:
            client.close()
            
            
        
    
    def updateUser(self, userName : str, name : str, userNameEdited : str, country : str, location:str, phoneNumber:str):
        try:
            client, collection, connectionStatus=User.connectDB()
            
            if connectionStatus is True: 
                    collection.update_one({'userName' : userName}, {'$set' : {'name' : name, 'phoneNumber': phoneNumber, 'country' : country, 'location': location, 'phoneNumber': phoneNumber, 'userName' : userNameEdited}})   
                    status="Profile update successfully"  
            else:
                status="Couldn't update profile"
                
            return status
        except Exception as e:
            logging.exception(e)
        finally:
            client.close()
    
    
    def setupIoT(self, userName:str, location:str, country:str, code:str):
        try:
            client, collection, connectionStatus=User.connectDB()
            
            if connectionStatus is True: 
                    collection.update_one({'userName' : userName}, {'$set' : { 'location': location, 'country' : country}})
                    collection.update_one({'userName' : userName}, {'$push' : { 'code' : code}})    
                    fieldData.createFieldDataTable(tableName=code)
                    return True
            else:
                return False
        except Exception as e:
            logging.exception(e)
               
        finally:
            client.close()
                
    def addIoT(self, userName:str, code:str):
        try:
            client, collection, connectionStatus=User.connectDB()
            
            if connectionStatus is True: 
                    collection.update_one({'userName' : userName}, {'$push' : { 'code' : code}})   
                    fieldData.createFieldDataTable(tableName=code)
                    status=True
            else:
                status=False
                
            return status  
        except Exception as e:
            logging.exception(e)            
        finally:
            client.close()
            
    
    
    def deleteIoT(self, userName:str, code:str):
        try:
            client, collection, connectionStatus=User.connectDB()
            
            if connectionStatus is True: 
                    collection.update_one({'userName' : userName}, {'$pull' : { 'code' : code}})    
                    fieldData.deleteFieldDataTable(tableName=code)
                    status=True
            else:
                status=False
                
                return status
        except Exception as e:
            logging.exception(e)
        finally:
            client.close()
    
    def editIoT(self, userName:str, code:str, newCode:str):
        try:
            client, collection, connectionStatus=User.connectDB()
            
            if connectionStatus is True: 
                    collection.update_one({'userName' : userName}, {'$pull' : { 'code' : code}})
                    collection.update_one({'userName' : userName}, {'$push' : { 'code' : newCode}})   
                    fieldData.editFieldDataTable(oldTableName=code, newTableName=newCode)     
                    status=True
            else:
                status=False
                
            return status
        except Exception as e:
            logging.exception(e)
        finally:
            client.close()
            
            
    def changePassword(self, userName:str, oldPassword:str, newPassword:str):
        try:
            client, collection, connectionStatus=User.connectDB()
            _, user=self.getUserByUserName(userName=userName)
            if user is None:
                status="User not found"
            else:
                isValid =self._bycrypt.check_password_hash(user['password'], oldPassword)
                if isValid:
                    newPassword=self._bycrypt.generate_password_hash(newPassword).decode('utf-8')
                    collection.update_one({'userName' : userName}, {'$set' : {'password' : newPassword}})
                    status='Password change successfully'
                else:
                    status='Can not change password' 
                    
                return status
        except Exception as e:
            logging.exception(e)  
        finally:
            client.close()
        
            
    

    def deleteUser(self, userName: str, password:str):
        try:
            client, collection, connectionStatus=User.connectDB()
            if connectionStatus is True:
                _, user=self.getUserByUserName(userName=userName)
                isValid =self._bycrypt.check_password_hash(user['password'], password)
                if isValid:
                    collection.delete_one({"userName" : userName})
                    status=True
                else:
                    status=False
            else:
                status=False
                
            return status

        except Exception as e:
            logging.exception(e)
        finally:
            client.close()
            
    

    def validatePassword(self, password : str):
        
        status="Valid password"
        
        if len(password) < 6:
            status="Password must contains at least 6 charactors"
        
        if not re.search(r'[a-z]', password):
            status="Password must contains at least one lowercase letter"

        if not re.search(r'[0-9]', password):
            status="Password must contains at least one digit"

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            status="Password must contain at least one special character"
        
        return status
        


        


    
        
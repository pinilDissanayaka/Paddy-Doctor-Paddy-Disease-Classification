from typing import TypedDict
import logging

logging.basicConfig(filename="log.log", level=logging.WARNING)

class IoTDataDict(TypedDict):
    date=[]
    potassium=[]
    nitrogen=[]
    phosphorus=[]
    temperature=[]
    humidity=[]
    soilMoisture=[]
    waterLevel=[]
    phLavel=[]
    
    
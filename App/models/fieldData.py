from database.database import Base, session, engine
from sqlalchemy import Column, String, Integer, Float, DateTime, BigInteger

Base.metadata.create_all(engine)


class FieldData(Base):
    __tablename__="fieldData"
    
    id=Column(BigInteger, primary_key=True, index=True)
    deviceID=Column(Integer)
    date=Column(DateTime())
    potassium=Column(Float(3, 3 ))
    nitrogen=Column(Float(3, 3 ))
    phosphorus=Column(Float(3, 3 ))
    temperature=Column(Float(3, 3 ))
    humidity=Column(Float(3, 3 ))
    soilMoisture=Column(Float(3, 3 ))
    waterLevel=Column(Float(3, 3 ))
    phLavel=Column(Float(3, 3 ))
    
    
    
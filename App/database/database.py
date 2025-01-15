import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv()

engine=create_engine(url=os.getenv('MYSQL_URL'))

Base=declarative_base()

localSession=sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base.metadata.create_all(engine)

session=localSession()
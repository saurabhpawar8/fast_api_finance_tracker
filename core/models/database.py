from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SQLALCHEMY_DATABASE_URL")


engine = create_engine(url,pool_size=10)
print("Database connection established")

SessionLocal=sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()
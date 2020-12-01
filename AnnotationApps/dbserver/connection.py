from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
dbpath = os.environ["DBPATH"]

conn_str = f"sqlite:///{dbpath}"
engine = create_engine(conn_str, connect_args={"check_same_thread": False})

print("connection is ok")

SessionDB = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

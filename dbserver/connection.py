from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import json
import os

assert "DBSETTINGS" in os.environ

dbsettings = json.load(open(os.environ["DBSETTINGS"]))
dbname = dbsettings["name"]
dbpath = dbsettings["path"]
dbsettings["schema"]["history"] = {
    "username": "string",
    "idx": "string",
    "done": "int"
}

conn_str = f"sqlite:///{dbpath}"
engine = create_engine(conn_str, echo=True, connect_args={"check_same_thread": False})

print("connection is ok")

SessionDB = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

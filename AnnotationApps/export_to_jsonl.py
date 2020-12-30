import sqlite3
import sys
import pandas as pd
import json

def load_json(value) :
    try :
        value = json.loads(value)
    except :
        pass

    return value

def read_db(dbpath, file_prefix) :
    con = sqlite3.connect(dbpath)
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';" , con)["name"].values
    for table in tables :
        data = pd.read_sql(f"SELECT * FROM {table}", con)
        data["value"] = data["value"].apply(load_json)
        data.to_json(f"{file_prefix}.{table}.jsonl", orient="records", lines=True)
        

if __name__ == "__main__" :
    dbpath = sys.argv[1]
    file_prefix = sys.argv[2]
    read_db(dbpath, file_prefix)

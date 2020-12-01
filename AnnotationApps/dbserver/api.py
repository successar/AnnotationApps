from AnnotationApps.dbserver.connection import SessionDB
import AnnotationApps.dbserver.models as models
from sqlalchemy.orm import scoped_session

session = scoped_session(SessionDB)

def add(tablename, keys, value):
    models.add(session, tablename, keys, value)


def delete(tablename, keys, value):
    models.delete(session, tablename, keys, value)


def filter_rows(tablename, keys):
    return models.filter_rows(session, table=tablename, keys=keys)

def get_value(tablename, keys) :
    rows = models.filter_rows(session, table=tablename, keys=keys)
    if len(rows) == 0:
        return None
    else :
        return rows[0]["value"]
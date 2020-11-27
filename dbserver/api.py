from AnnotationApps.dbserver.connection import SessionDB
import AnnotationApps.dbserver.models as models
from sqlalchemy.orm import scoped_session

session = scoped_session(SessionDB)

def add_or_delete(tablename, keys, value):
    models.add_or_delete(session, table=tablename, keys=keys, value=value)


def add_or_delete_multiple(tablename, common_keys, multi_keys):
    models.add_or_delete_multiple(session, tablename, common_keys, multi_keys)


def filter_rows(tablename, keys):
    return models.filter_rows(session, table=tablename, keys=keys)


def update(tablename, keys, update):
    models.update(session, tablename, keys, update)

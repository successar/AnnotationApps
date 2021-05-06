from AnnotationApps.dbserver.connection import Base, engine
from sqlalchemy import Column, Integer, PrimaryKeyConstraint, String

types_to_constructors = {
    int: lambda: Column(Integer),
    str: lambda: Column(String),
}

tables = {}


def create_table(name, columns):
    columns = {colname: types_to_constructors[coltype]() for colname, coltype in columns.items()}
    primary_key_columns = [v for v in columns.keys() if v != "value"]
    primary_key = {"__table_args__": (PrimaryKeyConstraint(*primary_key_columns), {},)}
    tables[name] = type(name, (Base,), {"__tablename__": name, **columns, **primary_key})
    tables[name].__table__.create(engine, checkfirst=True)


def exist_table(name):
    return name in tables


def add(ses, table, keys, value):
    assert all([key in keys or key == "value" for key in tables[table].__table__.columns.keys()])
    q = ses.query(tables[table]).filter_by(**keys).all()
    if len(q) == 0:
        ses.add(tables[table](**keys, value=value))
    else:
        if q[0].value != value :
            ses.query(tables[table]).filter_by(**keys).update({"value": value})

    ses.commit()


def delete(ses, table, keys):
    assert all([key in keys or key == "value" for key in tables[table].__table__.columns.keys()])
    ses.query(tables[table]).filter_by(**keys).delete()
    ses.commit()


def filter_rows(ses, table, keys):
    records = ses.query(tables[table]).filter_by(**keys).all()
    remaining_keys = [key for key in tables[table].__table__.columns.keys() if key not in keys]

    return [{key: getattr(r, key) for key in remaining_keys} for r in records]


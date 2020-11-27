from AnnotationApps.dbserver.connection import Base, engine, dbsettings
from sqlalchemy import Column, DateTime, Integer, PrimaryKeyConstraint, String

types_to_constructors = {
    "int": lambda: Column(Integer),
    "string": lambda: Column(String),
    "datetime": lambda: Column(DateTime),
}

tables = {}

for name, columns in dbsettings["schema"].items():
    columns = {colname: types_to_constructors[coltype]() for colname, coltype in columns.items()}
    primary_key = {"__table_args__": (PrimaryKeyConstraint(*columns.keys()), {},)}
    tables[name] = type(name, (Base,), {"__tablename__": name, **columns, **primary_key})

Base.metadata.create_all(engine)


def add_or_delete(ses, table, keys, value):
    assert all([key in keys for key in tables[table].__table__.columns.keys()])

    if value:
        ses.add(tables[table](**keys))
    else:
        ses.query(tables[table]).filter_by(**keys).delete()

    ses.commit()

    return {}


def add_or_delete_multiple(ses, table, keys, multikey):
    for subrow in multikey :
        rowkeys, val = subrow
        assert set(list(keys.keys()) + list(rowkeys.keys())) == set(list(tables[table].__table__.columns.keys()))
        if val:
            ses.add(tables[table](**{**rowkeys, **keys}))
        else:
            ses.query(tables[table]).filter_by(**{**rowkeys, **keys}).delete()

        ses.commit()

    return {}


def filter_rows(ses, table, keys):
    records = ses.query(tables[table]).filter_by(**keys).all()
    remaining_keys = [key for key in tables[table].__table__.columns.keys() if key not in keys]

    return [{key: getattr(r, key) for key in remaining_keys} for r in records]

def update(ses, table, keys, update_dict):
    ses.query(tables[table]).filter_by(**keys).update(update_dict)
    ses.commit()

    return {}


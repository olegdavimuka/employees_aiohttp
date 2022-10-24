from datetime import date

import aiopg.sa
from sqlalchemy import (Column, Date, ForeignKey, Integer, MetaData, String,
                        Table)

__all__ = ["employees", "positions"]

meta = MetaData()

employees = Table(
    "employees",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(255), nullable=False),
    Column(
        "position_id", Integer, ForeignKey("positions.id"), nullable=False, default=1
    ),
    Column("hire_date", Date, nullable=False, default=date.today()),
    Column("salary", Integer, nullable=False, default=0),
    Column("chief_id", Integer, ForeignKey("employees.id"), nullable=True, default=None),
)

positions = Table(
    "positions",
    meta,
    Column("id", Integer, primary_key=True),
    Column("name", String(255), nullable=False),
)


async def pg_context(app):
    conf = app["config"]["postgres"]
    engine = await aiopg.sa.create_engine(
        database=conf["database"],
        user=conf["user"],
        password=conf["password"],
        host=conf["host"],
        port=conf["port"],
        minsize=conf["minsize"],
        maxsize=conf["maxsize"],
    )
    app["db"] = engine

    yield

    app["db"].close()
    await app["db"].wait_closed()

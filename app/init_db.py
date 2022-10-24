from employees.db import employees, positions
from employees.settings import config
from sqlalchemy import MetaData, create_engine

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[employees, positions])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(
        positions.insert(),
        [
            {"name": "Junior"},
            {"name": "Middle"},
            {"name": "Senior"},
            {"name": "Lead"},
        ],
    )
    conn.execute(
        employees.insert(),
        [
            {
                "name": "Angus Dowling",
                "position_id": 4,
                "hire_date": "2019-01-01",
                "salary": 100000,
                "chief_id": None,
            },
            {
                "name": "Darius Andrade",
                "position_id": 3,
                "hire_date": "2020-01-01",
                "salary": 50000,
                "chief_id": 1,
            },
            {
                "name": "Amie Boone",
                "position_id": 3,
                "hire_date": "2020-01-01",
                "salary": 50000,
                "chief_id": 1,
            },
            {
                "name": "Vicky Ferry",
                "position_id": 2,
                "hire_date": "2021-01-01",
                "salary": 25000,
                "chief_id": 2,
            },
            {
                "name": "Derrick Goldsmith",
                "position_id": 2,
                "hire_date": "2021-01-01",
                "salary": 25000,
                "chief_id": 2,
            },
            {
                "name": "Lawrence Baker",
                "position_id": 2,
                "hire_date": "2021-01-01",
                "salary": 25000,
                "chief_id": 3,
            },
            {
                "name": "Dexter Greig",
                "position_id": 2,
                "hire_date": "2021-01-01",
                "salary": 25000,
                "chief_id": 3,
            },
            {
                "name": "Sapphire Conley",
                "position_id": 1,
                "hire_date": "2022-01-01",
                "salary": 10000,
                "chief_id": 4,
            },
            {
                "name": "Caitlyn Doyle",
                "position_id": 1,
                "hire_date": "2022-01-01",
                "salary": 10000,
                "chief_id": 4,
            },
            {
                "name": "Laibah Wilde",
                "position_id": 1,
                "hire_date": "2022-01-01",
                "salary": 10000,
                "chief_id": 5,
            },
            {
                "name": "Billy Bridges",
                "position_id": 1,
                "hire_date": "2022-01-01",
                "salary": 10000,
                "chief_id": 5,
            },
            {
                "name": "Donna Edmonds",
                "position_id": 1,
                "hire_date": "2022-01-01",
                "salary": 10000,
                "chief_id": 6,
            },
            {
                "name": "Jordyn Booker",
                "position_id": 1,
                "hire_date": "2022-01-01",
                "salary": 10000,
                "chief_id": 6,
            },
            {
                "name": "Julia Underwood",
                "position_id": 1,
                "hire_date": "2022-01-01",
                "salary": 10000,
                "chief_id": 7,
            },
            {
                "name": "Adina Swan",
                "position_id": 1,
                "hire_date": "2022-01-01",
                "salary": 10000,
                "chief_id": 7,
            },
        ],
    )
    conn.close()


if __name__ == "__main__":
    db_url = DSN.format(**config["postgres"])
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)

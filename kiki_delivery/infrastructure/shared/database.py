from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# todo: https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1
db_user = "mazuh"
db_password = ""
db_host = "localhost"
db_port = "5433"
db_name = "kiki_delivery"
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass

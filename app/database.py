from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.constants import constants_database


DATABASE_URL = f"mysql+pymysql://{constants_database["MYSQL_DATABASE"]}:{constants_database["MYSQL_USER"]}@{constants_database["MYSQL_HOST"]}:{int(constants_database["MYSQL_PORT"])}/{constants_database["MYSQL_DATABASE"]}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
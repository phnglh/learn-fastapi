from sqlalchemy.exc import OperationalError
from src.core.config import settings
from sqlmodel import SQLModel,Session,create_engine

engine = create_engine(str(settings.SQLMODEL_DATABASE_URI()))

def init_db() -> None:
    SQLModel.metadata.create_all(bind=engine)

def check_connection():
    try:
        with engine.connect() as conn:
            print("✅ Database connected successfully!")
    except OperationalError as e:
        print("❌ Database connection failed:", e)
        raise

from fastapi import FastAPI
from src.core.database import check_connection,init_db

app = FastAPI(root_path="/api")

if __name__ == "__main__":
    check_connection()
    init_db()

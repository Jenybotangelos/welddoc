import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc:///?odbc_connect="
        + os.getenv("AZURE_SQL_CONNECTION_STRING", "")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

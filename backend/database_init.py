# database_init.py
import sqlalchemy
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine
engine = create_engine(DATABASE_URL)

# Define metadata
metadata = sqlalchemy.MetaData()

# Define table
reports = sqlalchemy.Table(
    "reports",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime),
    sqlalchemy.Column("transcript", sqlalchemy.Text),
    sqlalchemy.Column("medical_entities", sqlalchemy.JSON),
    sqlalchemy.Column("analysis", sqlalchemy.JSON)
)

def init_db():
    """Initialize the database"""
    try:
        metadata.create_all(engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    init_db()
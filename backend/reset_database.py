# reset_database.py
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, DateTime, Text, JSON
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine
engine = create_engine(DATABASE_URL)
metadata = MetaData()

def reset_db():
    # Drop all tables
    metadata.reflect(bind=engine)
    metadata.drop_all(engine)
    print("Dropped all existing tables")

    # Create reports table with all columns
    reports = Table(
        "reports",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("timestamp", DateTime),
        Column("transcript", Text),
        Column("medical_entities", JSON),
        Column("analysis", JSON)
    )

    # Create the table
    metadata.create_all(engine)
    print("Created new reports table with all columns")

if __name__ == "__main__":
    reset_db()
# database_init.py
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, DateTime, Text, JSON

# Database configuration
DATABASE_URL = "postgresql://habari:habari@localhost/medical_reports"

# Create engine
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define the reports table
reports = Table(
    "reports",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("timestamp", DateTime),
    Column("transcript", Text),
    Column("medical_entities", JSON)
)

def init_db():
    metadata.create_all(engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
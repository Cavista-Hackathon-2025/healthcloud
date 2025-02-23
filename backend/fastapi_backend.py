from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import databases
import sqlalchemy
from sqlalchemy import JSON, create_engine
import logging
import os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Database configuration
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Define database model with combined report and analysis
reports = sqlalchemy.Table(
    "reports",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime),
    sqlalchemy.Column("transcript", sqlalchemy.Text),
    sqlalchemy.Column("medical_entities", sqlalchemy.JSON),
    sqlalchemy.Column("analysis", sqlalchemy.JSON)
)

# Create tables
engine = create_engine(DATABASE_URL)
try:
    metadata.create_all(engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating tables: {e}")

# Pydantic models
class MedicalEntities(BaseModel):
    conditions: List[str]
    medications: List[str]
    symptoms: List[str]
    procedures: List[str]

class Analysis(BaseModel):
    symptoms: Dict
    severity: Dict
    urgency: Dict

class Report(BaseModel):
    timestamp: datetime
    transcript: str
    medical_entities: MedicalEntities
    analysis: Analysis

app = FastAPI()

@app.on_event("startup")
async def startup():
    try:
        await database.connect()
        logger.info("Database connected successfully")
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise

@app.on_event("shutdown")
async def shutdown():
    try:
        await database.disconnect()
        logger.info("Database disconnected successfully")
    except Exception as e:
        logger.error(f"Error disconnecting from database: {e}")

@app.get("/api/reports/", response_model=List[Report])
async def get_reports():
    try:
        query = reports.select()
        result = await database.fetch_all(query)
        logger.info(f"Retrieved {len(result) if result else 0} reports")
        return result
    except Exception as e:
        logger.error(f"Error retrieving reports: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reports/", response_model=Report)
async def create_report(report: Report):
    try:
        query = reports.insert().values(
            timestamp=report.timestamp,
            transcript=report.transcript,
            medical_entities=report.medical_entities.dict(),
            analysis=report.analysis.dict()
        )
        last_record_id = await database.execute(query)
        return {**report.dict(), "id": last_record_id}
    except Exception as e:
        logger.error(f"Error creating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
async def test_endpoint():
    return {"status": "API is running"}

@app.get("/test-db")
async def test_database():
    try:
        await database.fetch_one("SELECT 1")
        return {"status": "Database connection successful"}
    except Exception as e:
        logger.error(f"Database test failed: {e}")
        return {"status": "Database connection failed", "error": str(e)}

@app.get("/api/reports/{report_id}", response_model=Report)
async def get_report(report_id: int):
    try:
        query = reports.select().where(reports.c.id == report_id)
        result = await database.fetch_one(query)
        
        if result is None:
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Format and return the report
        report = {
            "id": result.id,
            "timestamp": result.timestamp,
            "transcript": result.transcript,
            "medical_entities": result.medical_entities,
            "analysis": result.analysis
        }
        logger.info(f"Retrieved report {report_id}")
        return report
    except Exception as e:
        logger.error(f"Error retrieving report: {e}")
        raise HTTPException(status_code=500, detail=str(e))
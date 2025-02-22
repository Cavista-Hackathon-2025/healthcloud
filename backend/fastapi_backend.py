# fastapi_backend.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import databases
import sqlalchemy
from sqlalchemy import JSON, create_engine, ForeignKey
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

# Define database models
reports = sqlalchemy.Table(
    "reports",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime),
    sqlalchemy.Column("transcript", sqlalchemy.Text),
    sqlalchemy.Column("medical_entities", sqlalchemy.JSON)
)

ai_analyses = sqlalchemy.Table(
    "ai_analyses",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("report_id", sqlalchemy.Integer, ForeignKey("reports.id")),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime),
    sqlalchemy.Column("symptoms", sqlalchemy.JSON),
    sqlalchemy.Column("medical_history", sqlalchemy.JSON),
    sqlalchemy.Column("severity", sqlalchemy.JSON),
    sqlalchemy.Column("urgency", sqlalchemy.JSON)
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

class Report(BaseModel):
    timestamp: datetime
    transcript: str
    medical_entities: MedicalEntities

class Analysis(BaseModel):
    report_id: int
    timestamp: datetime
    symptoms: Dict
    medical_history: Dict
    severity: Dict
    urgency: Dict

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

# Report endpoints
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

@app.get("/api/reports/{report_id}", response_model=Report)
async def get_report(report_id: int):
    try:
        query = reports.select().where(reports.c.id == report_id)
        result = await database.fetch_one(query)
        
        if result is None:
            raise HTTPException(status_code=404, detail="Report not found")
            
        return result
    except Exception as e:
        logger.error(f"Error retrieving report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reports/", response_model=Report)
async def create_report(report: Report):
    try:
        query = reports.insert().values(
            timestamp=report.timestamp,
            transcript=report.transcript,
            medical_entities=report.medical_entities.dict()
        )
        last_record_id = await database.execute(query)
        logger.info("Report created successfully")
        return {**report.dict(), "id": last_record_id}
    except Exception as e:
        logger.error(f"Error creating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# AI Analysis endpoints
@app.get("/api/analyses/", response_model=List[Analysis])
async def get_analyses():
    try:
        query = ai_analyses.select()
        result = await database.fetch_all(query)
        logger.info(f"Retrieved {len(result) if result else 0} analyses")
        return result
    except Exception as e:
        logger.error(f"Error retrieving analyses: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analyses/{report_id}", response_model=Analysis)
async def get_analysis_by_report(report_id: int):
    try:
        query = ai_analyses.select().where(ai_analyses.c.report_id == report_id)
        result = await database.fetch_one(query)
        
        if result is None:
            raise HTTPException(status_code=404, detail="Analysis not found")
            
        return result
    except Exception as e:
        logger.error(f"Error retrieving analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyses/", response_model=Analysis)
async def create_analysis(analysis: Analysis):
    try:
        # Verify report exists
        report_query = reports.select().where(reports.c.id == analysis.report_id)
        report = await database.fetch_one(report_query)
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        query = ai_analyses.insert().values(
            report_id=analysis.report_id,
            timestamp=analysis.timestamp,
            symptoms=analysis.symptoms,
            medical_history=analysis.medical_history,
            severity=analysis.severity,
            urgency=analysis.urgency
        )
        last_record_id = await database.execute(query)
        logger.info(f"Analysis created for report {analysis.report_id}")
        return {**analysis.dict(), "id": last_record_id}
    except Exception as e:
        logger.error(f"Error creating analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Test endpoints
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
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import databases
import sqlalchemy
import os
from dotenv import load_dotenv



# Database configuration
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

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/api/reports/", response_model=Report)
async def create_report(report: Report):
    query = reports.insert().values(
        timestamp=report.timestamp,
        transcript=report.transcript,
        medical_entities=report.medical_entities.dict()
    )
    await database.execute(query)
    return report

@app.get("/api/reports/", response_model=List[Report])
async def get_reports():
    query = reports.select()
    return await database.fetch_all(query)

@app.get("/api/reports/{report_id}", response_model=Report)
async def get_report(report_id: int):
    query = reports.select().where(reports.c.id == report_id)
    report = await database.fetch_one(query)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
# fastapi_backend.py
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import databases
import sqlalchemy
from sqlalchemy import JSON, create_engine, ForeignKey
import logging
import os
from dotenv import load_dotenv
import whisper
import tempfile
import os
import nltk
import spacy

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

# Load Whisper model (do this once when the server starts)
whisper_model = whisper.load_model("base")

# Load spaCy model for medical entity extraction
nlp = spacy.load("en_core_web_sm")

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

def extract_medical_entities(text):
    """Extract medical entities from transcribed text"""
    doc = nlp(text)
    
    medical_entities = {
        "conditions": [],
        "medications": [],
        "symptoms": [],
        "procedures": []
    }
    
    # Simple entity extraction
    for ent in doc.ents:
        if ent.label_ in ["DISEASE", "CONDITION", "MEDICAL_CONDITION"]:
            medical_entities["conditions"].append(ent.text)
        elif ent.label_ in ["DRUG", "MEDICATION"]:
            medical_entities["medications"].append(ent.text)
        elif ent.label_ in ["SYMPTOM"]:
            medical_entities["symptoms"].append(ent.text)
        elif ent.label_ in ["PROCEDURE", "TREATMENT"]:
            medical_entities["procedures"].append(ent.text)
    
    return medical_entities

def analyze_medical_content(text):
    """Analyze medical content for severity and urgency"""
    # Simple keyword-based analysis
    severity_keywords = {
        "severe": ["severe", "intense", "extreme", "worst"],
        "moderate": ["moderate", "significant", "uncomfortable"],
        "mild": ["mild", "slight", "minor"]
    }

    urgency_keywords = {
        "emergency": ["emergency", "immediately", "severe pain", "chest pain"],
        "urgent": ["urgent", "worrying", "getting worse"],
        "routine": ["routine", "chronic", "ongoing"]
    }

    text_lower = text.lower()
    
    # Determine severity
    severity = {"level": "mild", "confidence": 0.5}
    for level, keywords in severity_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            severity = {"level": level, "confidence": 0.8}
            break

    # Determine urgency
    urgency = {"level": "routine", "confidence": 0.5}
    for level, keywords in urgency_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            urgency = {"level": level, "confidence": 0.8}
            break

    return {
        "symptoms": extract_medical_entities(text),
        "severity": severity,
        "urgency": urgency
    }
    
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
        # Log the incoming analysis data for debugging
        logger.debug(f"Received analysis data: {analysis}")
        
        # Verify report exists
        report_query = reports.select().where(reports.c.id == analysis.report_id)
        report = await database.fetch_one(report_query)
        
        if not report:
            logger.error(f"Report not found for ID: {analysis.report_id}")
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Convert Pydantic model to dictionary, ensuring all fields are properly serialized
        analysis_dict = {
            "report_id": analysis.report_id,
            "timestamp": analysis.timestamp,
            "symptoms": dict(analysis.symptoms) if analysis.symptoms else {},
            "medical_history": dict(analysis.medical_history) if analysis.medical_history else {},
            "severity": dict(analysis.severity) if analysis.severity else {},
            "urgency": dict(analysis.urgency) if analysis.urgency else {}
        }
        
        # Detailed logging of the dictionary to be inserted
        logger.debug(f"Prepared analysis dictionary: {analysis_dict}")
        
        query = ai_analyses.insert().values(**analysis_dict)
        
        try:
            last_record_id = await database.execute(query)
            logger.info(f"Analysis created successfully for report {analysis.report_id}. Record ID: {last_record_id}")
            return {**analysis_dict, "id": last_record_id}
        except Exception as db_error:
            logger.error(f"Database insertion error: {db_error}")
            raise HTTPException(status_code=500, detail=f"Database insertion failed: {str(db_error)}")
    
    except Exception as e:
        logger.error(f"Comprehensive error creating analysis: {e}")
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

@app.post("/api/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    try:
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(await audio.read())
            temp_audio_path = temp_audio.name

        # Transcribe audio
        result = whisper_model.transcribe(temp_audio_path)
        transcript = result["text"]

        # Extract medical entities
        medical_entities = extract_medical_entities(transcript)

        # Create report
        report_data = {
            "timestamp": datetime.now(),
            "transcript": transcript,
            "medical_entities": medical_entities
        }
        report = await create_report(Report(**report_data))

        # Analyze medical content
        analysis_data = analyze_medical_content(transcript)
        
        # Create analysis
        full_analysis_data = {
            "report_id": report["id"],
            "timestamp": datetime.now(),
            "symptoms": analysis_data["symptoms"],
            "medical_history": {"detected_conditions": medical_entities.get("conditions", [])},
            "severity": analysis_data["severity"],
            "urgency": analysis_data["urgency"]
        }
        analysis = await create_analysis(Analysis(**full_analysis_data))

        # Clean up temporary file
        os.unlink(temp_audio_path)

        return {
            "transcript": transcript,
            "report_id": report["id"],
            "analysis_id": analysis["id"],
            "medical_entities": medical_entities
        }

    except Exception as e:
        logger.error(f"Transcription error: {e}")
        # Clean up temp file if it exists
        if 'temp_audio_path' in locals() and os.path.exists(temp_audio_path):
            os.unlink(temp_audio_path)
        raise HTTPException(status_code=500, detail=str(e))
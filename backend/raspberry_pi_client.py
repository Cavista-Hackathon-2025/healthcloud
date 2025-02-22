import sounddevice as sd
import numpy as np
import requests
import json
import whisper
import spacy
from datetime import datetime

class AudioProcessor:
    def __init__(self):
        self.model = whisper.load_model("base")
        self.nlp = spacy.load("en_core_sci_md")  # Medical-specific NLP model
        self.api_url = "http://localhost:8000/api/reports"
        
    def record_audio(self, duration=60, sample_rate=16000):
        """Record audio from microphone"""
        print("Recording...")
        audio = sd.rec(int(duration * sample_rate),
                      samplerate=sample_rate,
                      channels=1,
                      dtype='float32')
        sd.wait()
        return audio
        
    def transcribe_audio(self, audio):
        """Convert audio to text using Whisper"""
        result = self.model.transcribe(audio)
        return result["text"]
        
    def extract_medical_info(self, text):
        """Extract medical entities and key information"""
        doc = self.nlp(text)
        
        # Extract medical entities
        medical_entities = {
            "conditions": [],
            "medications": [],
            "symptoms": [],
            "procedures": []
        }
        
        for ent in doc.ents:
            if ent.label_ == "CONDITION":
                medical_entities["conditions"].append(ent.text)
            elif ent.label_ == "MEDICATION":
                medical_entities["medications"].append(ent.text)
            elif ent.label_ == "SYMPTOM":
                medical_entities["symptoms"].append(ent.text)
            elif ent.label_ == "PROCEDURE":
                medical_entities["procedures"].append(ent.text)
        
        return medical_entities
        
    def send_to_api(self, report_data):
        """Send processed report to FastAPI backend"""
        try:
            response = requests.post(
                self.api_url,
                json=report_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending data to API: {e}")
            return None

    def process_conversation(self):
        """Main processing pipeline"""
        # Record audio
        audio = self.record_audio()
        
        # Transcribe
        transcript = self.transcribe_audio(audio)
        
        # Extract medical information
        medical_info = self.extract_medical_info(transcript)
        
        # Create report
        report = {
            "timestamp": datetime.now().isoformat(),
            "transcript": transcript,
            "medical_entities": medical_info
        }
        
        # Send to API
        result = self.send_to_api(report)
        return result
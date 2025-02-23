# raspberry_pi_processor.py
import sounddevice as sd
import numpy as np
import requests
import json
import whisper
import spacy
from datetime import datetime
import soundfile as sf
import tempfile

class AudioProcessor:
    def __init__(self):
        print("Loading Whisper model...")
        self.model = whisper.load_model("base")
        print("Loading spaCy model...")
        self.nlp = spacy.load("en_core_web_sm")  
        self.api_url = "http://localhost:8000/api"
        print("System ready!")
        
    def record_audio(self):
        """Record audio from microphone until stopped"""
        print("\n" + "="*50)
        print("Recording... Press Ctrl+C to stop")
        print("Please speak now...")
        
        audio_chunks = []
        self.recording = True

        def audio_callback(indata, frames, time, status):
            if status:
                print(status)
            audio_chunks.append(indata.copy())

        with sd.InputStream(samplerate=16000, channels=1, callback=audio_callback):
            try:
                while self.recording:
                    sd.sleep(100)
            except KeyboardInterrupt:
                self.recording = False
                print("\nRecording stopped!")
                print("="*50 + "\n")

        if audio_chunks:
            audio = np.concatenate(audio_chunks, axis=0)
            return audio
        return None

    def save_audio(self, audio):
        """Save audio to temporary file"""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            sf.write(temp_audio.name, audio, 16000)
            return temp_audio.name
        
    def transcribe_audio(self, audio_path):
        """Convert audio to text using Whisper"""
        print("Transcribing audio...")
        result = self.model.transcribe(audio_path)
        print("\nTRANSCRIPTION:")
        print("-"*50)
        print(result["text"])
        print("-"*50 + "\n")
        return result["text"]
        
    def extract_medical_info(self, text):
        """Extract medical entities and key information"""
        print("Extracting medical information...")
        doc = self.nlp(text)
        
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
        
        print("\nExtracted Medical Entities:")
        print(json.dumps(medical_entities, indent=2))
        return medical_entities

    def analyze_medical_content(self, text):
        """Analyze medical content for severity and urgency"""
        # Simple keyword-based analysis for severity
        severity_keywords = {
            "severe": ["severe", "intense", "extreme", "worst"],
            "moderate": ["moderate", "significant", "uncomfortable"],
            "mild": ["mild", "slight", "minor"]
        }

        # Simple keyword-based analysis for urgency
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
            "symptoms": self.extract_medical_info(text),
            "severity": severity,
            "urgency": urgency
        }
        
    def send_to_api(self, endpoint, data):
        """Send data to API endpoint"""
        try:
            url = f"{self.api_url}/{endpoint}"
            response = requests.post(
                url,
                json=data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending data to API: {e}")
            if hasattr(e, 'response'):
                print("Error details:", e.response.text)
            return None

    def process_conversation(self):
        """Main processing pipeline"""
        try:
            # Record audio
            audio = self.record_audio()
            
            if audio is not None:
                # Save audio to file
                audio_path = self.save_audio(audio)
                
                # Transcribe
                transcript = self.transcribe_audio(audio_path)
                
                # Create and send report
                report_data = {
                    "timestamp": datetime.now().isoformat(),
                    "transcript": transcript,
                    "medical_entities": self.extract_medical_info(transcript)
                }
                
                report_response = self.send_to_api("reports", report_data)
                
                if report_response:
                    report_id = report_response["id"]
                    print(f"\nReport created with ID: {report_id}")
                    
                    # Analyze and send analysis
                    analysis = self.analyze_medical_content(transcript)
                    analysis_data = {
                        "report_id": report_id,
                        "timestamp": datetime.now().isoformat(),
                        "symptoms": analysis["symptoms"],
                        "severity": analysis["severity"],
                        "urgency": analysis["urgency"]
                    }
                    
                    analysis_response = self.send_to_api("analyses", analysis_data)
                    if analysis_response:
                        print("\nAnalysis created successfully")
                        return report_response, analysis_response
                    
            return None
            
        except Exception as e:
            print(f"Error in processing pipeline: {e}")
            return None

def main():
    processor = AudioProcessor()
    print("\nStarting medical transcription system...")
    print("Press Ctrl+C to stop recording when finished speaking")
    processor.process_conversation()

if __name__ == "__main__":
    main()
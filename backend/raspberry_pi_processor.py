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
        
        # Medical keywords for analysis
        self.medical_terms = {
            "severity_keywords": {
                "severe": ["severe", "intense", "extreme", "worst"],
                "moderate": ["moderate", "significant", "uncomfortable"],
                "mild": ["mild", "slight", "minor"]
            },
            "urgency_keywords": {
                "emergency": ["emergency", "immediately", "severe pain", "chest pain"],
                "urgent": ["urgent", "worrying", "getting worse"],
                "routine": ["routine", "chronic", "ongoing"]
            }
        }
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
        
        return medical_entities

    def analyze_medical_content(self, text):
        """Analyze medical content for severity and urgency"""
        text_lower = text.lower()
        medical_info = self.extract_medical_info(text)
        
        # Determine severity
        severity = {"level": "mild", "confidence": 0.5}
        for level, keywords in self.medical_terms["severity_keywords"].items():
            if any(keyword in text_lower for keyword in keywords):
                severity = {"level": level, "confidence": 0.8}
                break

        # Determine urgency
        urgency = {"level": "routine", "confidence": 0.5}
        for level, keywords in self.medical_terms["urgency_keywords"].items():
            if any(keyword in text_lower for keyword in keywords):
                urgency = {"level": level, "confidence": 0.8}
                break

        # Print analysis report
        self._print_analysis_report(medical_info, severity, urgency)

        return {
            "symptoms": medical_info,
            "severity": severity,
            "urgency": urgency
        }

    def _print_analysis_report(self, medical_info, severity, urgency):
        """Print formatted analysis report"""
        print("\nMEDICAL ANALYSIS REPORT")
        print("=" * 50)

        if any(medical_info["symptoms"]):
            print("\nSYMPTOMS IDENTIFIED:")
            for symptom in medical_info["symptoms"]:
                print(f"- {symptom}")
        
        if any(medical_info["conditions"]):
            print("\nMEDICAL CONDITIONS:")
            for condition in medical_info["conditions"]:
                print(f"- {condition}")

        print("\nSEVERITY ASSESSMENT:")
        print(f"Level: {severity['level'].upper()}")
        print(f"Confidence: {severity['confidence']*100:.1f}%")

        print("\nURGENCY ASSESSMENT:")
        print(f"Level: {urgency['level'].upper()}")
        
        print("\nRECOMMENDATIONS:")
        if urgency['level'] == 'emergency':
            print("- IMMEDIATE MEDICAL ATTENTION REQUIRED")
            print("- Emergency services should be contacted")
        elif urgency['level'] == 'urgent':
            print("- Urgent medical consultation recommended")
            print("- Follow-up within 24-48 hours")
        else:
            print("- Routine follow-up recommended")
            print("- Monitor symptoms for changes")

        print("=" * 50)

    def send_to_api(self, data):
        """Send data to API"""
        try:
            url = f"{self.api_url}/reports"
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
            audio = self.record_audio()
            
            if audio is not None:
                audio_path = self.save_audio(audio)
                transcript = self.transcribe_audio(audio_path)
                
                # Get analysis right after transcription
                analysis = self.analyze_medical_content(transcript)
                
                # Prepare combined report data
                report_data = {
                    "timestamp": datetime.now().isoformat(),
                    "transcript": transcript,
                    "medical_entities": self.extract_medical_info(transcript),
                    "analysis": analysis
                }
                
                # Send to API
                response = self.send_to_api(report_data)
                if response:
                    print("\nReport and analysis saved successfully")
                    return response
                    
            return None
            
        except Exception as e:
            print(f"\nError: {str(e)}")
            return None

def main():
    processor = AudioProcessor()
    print("\nStarting medical transcription system...")
    print("Press Ctrl+C to stop recording when finished speaking")
    processor.process_conversation()

if __name__ == "__main__":
    main()
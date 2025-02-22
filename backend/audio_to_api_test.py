# audio_to_api_test.py
import sounddevice as sd
import numpy as np
import requests
from datetime import datetime
import wave
import whisper
import tempfile
import soundfile as sf

class AudioProcessor:
    def __init__(self):
        self.api_url = "http://localhost:8000/api/reports"
        print("Loading Whisper model...")
        self.model = whisper.load_model("base")
        print("Whisper model loaded!")
        
    def record_audio(self, duration=5, sample_rate=16000):
        """Record audio from microphone"""
        print("\n" + "="*50)
        print(f"Recording for {duration} seconds...")
        print("Please speak now...")
        audio = sd.rec(int(duration * sample_rate),
                      samplerate=sample_rate,
                      channels=1,
                      dtype='float32')
        sd.wait()
        print("Recording finished!")
        print("="*50 + "\n")
        return audio, sample_rate

    def save_audio(self, audio, sample_rate):
        """Save audio to a temporary file"""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            sf.write(temp_audio.name, audio, sample_rate)
            return temp_audio.name

    def transcribe_audio(self, audio_path):
        """Transcribe audio using Whisper"""
        print("Transcribing audio...")
        result = self.model.transcribe(audio_path)
        print("\nTRANSCRIPTION OUTPUT:")
        print("-"*50)
        print(result["text"])
        print("-"*50 + "\n")
        return result["text"]

    def extract_medical_entities(self, text):
        """Simple medical entity extraction"""
        print("Extracting medical entities...")
        medical_entities = {
            "conditions": [],
            "medications": [],
            "symptoms": [],
            "procedures": []
        }
        
        # Simple keyword matching
        text_lower = text.lower()
        
        # Symptoms
        for symptom in ["headache", "pain", "nausea", "fever", "cough"]:
            if symptom in text_lower:
                medical_entities["symptoms"].append(symptom)
        
        # Medications
        for med in ["ibuprofen", "paracetamol", "aspirin"]:
            if med in text_lower:
                medical_entities["medications"].append(med)
                
        # Conditions
        for condition in ["flu", "cold", "migraine", "covid"]:
            if condition in text_lower:
                medical_entities["conditions"].append(condition)
                
        print("\nExtracted Entities:")
        for category, items in medical_entities.items():
            if items:
                print(f"{category.capitalize()}: {', '.join(items)}")
        print()
        
        return medical_entities

    def send_to_api(self, report_data):
        """Send processed report to API"""
        try:
            print("Sending report to API...")
            response = requests.post(
                self.api_url,
                json=report_data,
                headers={"Content-Type": "application/json"}
            )
            print("\nAPI Response:")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.json()
        except Exception as e:
            print(f"\nError sending to API: {e}")
            return None

    def process_and_send(self):
        """Main processing pipeline"""
        try:
            # Record audio
            audio, sample_rate = self.record_audio(duration=5)
            
            # Save to temporary file
            audio_path = self.save_audio(audio, sample_rate)
            
            # Transcribe
            transcript = self.transcribe_audio(audio_path)
            
            # Extract medical entities
            medical_entities = self.extract_medical_entities(transcript)
            
            # Create report
            report = {
                "timestamp": datetime.now().isoformat(),
                "transcript": transcript,
                "medical_entities": medical_entities
            }
            
            # Send to API
            result = self.send_to_api(report)
            
            return result
            
        except Exception as e:
            print(f"\nError in processing pipeline: {e}")
            return None

def main():
    print("\nInitializing Audio Processing System...")
    processor = AudioProcessor()
    print("\nSystem ready! Starting new recording session...")
    processor.process_and_send()

if __name__ == "__main__":
    main()
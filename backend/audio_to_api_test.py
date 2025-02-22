# audio_to_api_test.py
import sounddevice as sd
import numpy as np
import requests
from datetime import datetime
import wave
import whisper
import tempfile
import soundfile as sf
import threading
import queue
import signal
import sys

class AudioProcessor:
    def __init__(self):
        self.api_url = "http://localhost:8000/api/reports"
        print("Loading Whisper model...")
        self.model = whisper.load_model("base")
        print("Whisper model loaded!")
        self.recording = False
        self.audio_queue = queue.Queue()
        
    def record_audio(self, sample_rate=16000):
        """Record audio from microphone until stopped"""
        print("\n" + "="*50)
        print("Recording... Press Ctrl+C to stop")
        print("Please speak now...")
        
        # Initialize an empty list to store audio chunks
        audio_chunks = []
        self.recording = True

        def audio_callback(indata, frames, time, status):
            if status:
                print(status)
            audio_chunks.append(indata.copy())

        # Start the recording stream
        with sd.InputStream(samplerate=sample_rate, channels=1, callback=audio_callback):
            try:
                while self.recording:
                    sd.sleep(100)  # Sleep to prevent busy-waiting
            except KeyboardInterrupt:
                self.recording = False
                print("\nRecording stopped!")
                print("="*50 + "\n")

        # Combine all audio chunks
        if audio_chunks:
            audio = np.concatenate(audio_chunks, axis=0)
            return audio, sample_rate
        return None, None

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
        for symptom in ["headache", "pain", "nausea", "fever", "cough", "dizziness", 
                       "fatigue", "vomiting", "chest pain", "shortness of breath"]:
            if symptom in text_lower:
                medical_entities["symptoms"].append(symptom)
        
        # Medications
        for med in ["ibuprofen", "paracetamol", "aspirin", "acetaminophen", 
                   "amoxicillin", "penicillin", "antibiotic"]:
            if med in text_lower:
                medical_entities["medications"].append(med)
                
        # Conditions
        for condition in ["flu", "cold", "migraine", "covid", "diabetes", 
                         "hypertension", "asthma", "allergies"]:
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
            audio, sample_rate = self.record_audio()
            
            if audio is not None:
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
            else:
                print("No audio recorded.")
                return None
            
        except Exception as e:
            print(f"\nError in processing pipeline: {e}")
            return None

def main():
    print("\nInitializing Audio Processing System...")
    processor = AudioProcessor()
    print("\nSystem ready! Starting new recording session...")
    print("Press Ctrl+C to stop recording when finished speaking")
    processor.process_and_send()

if __name__ == "__main__":
    main()
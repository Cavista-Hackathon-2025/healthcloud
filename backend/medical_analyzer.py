# medical_analyzer_system.py
import sounddevice as sd
import soundfile as sf
import numpy as np
import whisper
from transformers import pipeline
import spacy
import tempfile
from datetime import datetime
import requests
import json

class MedicalAnalyzerSystem:
    def __init__(self):
        print("Loading Whisper model...")
        self.whisper_model = whisper.load_model("base")
        
        print("Loading classification model...")
        self.classifier = pipeline("zero-shot-classification", 
                                 model="facebook/bart-large-mnli")
        
        self.nlp = spacy.load('en_core_web_sm')
        self.api_url = "http://localhost:8000/api/reports"
        
        # Medical terms for entity extraction
        self.medical_terms = {
            "symptoms": [
                "pain", "ache", "nausea", "fever", "headache", "dizzy",
                "fatigue", "cough", "breathing", "vomiting", "swelling"
            ],
            "conditions": [
                "diabetes", "hypertension", "asthma", "migraine",
                "arthritis", "infection", "flu", "cold"
            ],
            "medications": [
                "ibuprofen", "paracetamol", "aspirin", "antibiotic",
                "medicine", "tablet", "prescription"
            ],
            "procedures": [
                "surgery", "operation", "scan", "x-ray", "test",
                "examination", "check-up"
            ]
        }
        
        print("System ready!")

    def record_audio(self, sample_rate=16000):
        """Record audio until stopped"""
        print("\n" + "="*50)
        print("Recording... Press Ctrl+C to stop")
        print("Please speak now...")
        
        audio_chunks = []
        self.recording = True

        def audio_callback(indata, frames, time, status):
            if status:
                print(status)
            audio_chunks.append(indata.copy())

        with sd.InputStream(samplerate=sample_rate, channels=1, callback=audio_callback):
            try:
                while self.recording:
                    sd.sleep(100)
            except KeyboardInterrupt:
                self.recording = False
                print("\nRecording stopped!")
                print("="*50 + "\n")

        if audio_chunks:
            audio = np.concatenate(audio_chunks, axis=0)
            return audio, sample_rate
        return None, None

    def transcribe_audio(self, audio_path):
        """Transcribe audio using Whisper"""
        print("Transcribing audio...")
        result = self.whisper_model.transcribe(audio_path)
        
        print("\nTRANSCRIPTION:")
        print("-"*50)
        print(result["text"])
        print("-"*50 + "\n")
        
        return result["text"]

    def extract_medical_entities(self, text):
        """Extract medical entities using predefined categories"""
        text_lower = text.lower()
        entities = {
            "conditions": [],
            "medications": [],
            "symptoms": [],
            "procedures": []
        }
        
        # Extract entities for each category
        for category in self.medical_terms:
            for term in self.medical_terms[category]:
                if term in text_lower:
                    entities[category].append(term)
        
        return entities

    def analyze_with_zero_shot(self, text):
        """Additional AI analysis using zero-shot classification"""
        analysis_categories = {
            "urgency": ["emergency", "urgent", "non-urgent", "routine"],
            "severity": ["mild", "moderate", "severe"],
            "follow_up": ["immediate", "short-term", "routine"]
        }
        
        ai_analysis = {}
        for category, labels in analysis_categories.items():
            result = self.classifier(text, candidate_labels=labels)
            ai_analysis[category] = {
                "classification": result["labels"][0],
                "confidence": result["scores"][0]
            }
        
        return ai_analysis

    def save_audio(self, audio, sample_rate):
        """Save audio to a temporary file"""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            sf.write(temp_audio.name, audio, sample_rate)
            return temp_audio.name

    def send_to_api(self, report_data):
        """Send report data to API"""
        try:
            response = requests.post(
                self.api_url,
                json=report_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            print("\nSuccessfully sent to API!")
            return response.json()
        except Exception as e:
            print(f"\nError sending to API: {e}")
            if hasattr(e.response, 'text'):
                print("Error details:", e.response.text)
            return None

    def process_consultation(self):
        """Main processing pipeline"""
        try:
            # Record audio
            audio, sample_rate = self.record_audio()
            
            if audio is not None:
                # Save audio to file
                audio_path = self.save_audio(audio, sample_rate)
                
                # Transcribe audio
                transcript = self.transcribe_audio(audio_path)
                
                # Extract medical entities
                medical_entities = self.extract_medical_entities(transcript)
                
                # Perform AI analysis
                ai_analysis = self.analyze_with_zero_shot(transcript)
                
                # Prepare report
                report = {
                    "timestamp": datetime.now().isoformat(),
                    "transcript": transcript,
                    "medical_entities": medical_entities
                }
                
                # Send to API
                result = self.send_to_api(report)
                
                # Print results
                print("\nMedical Entities:")
                print(json.dumps(medical_entities, indent=2))
                print("\nAI Analysis:")
                print(json.dumps(ai_analysis, indent=2))
                
                return result
            
        except Exception as e:
            print(f"Error in processing pipeline: {e}")
            return None

def main():
    analyzer = MedicalAnalyzerSystem()
    print("\nStarting medical consultation analysis...")
    print("Press Ctrl+C to stop recording when finished speaking")
    analyzer.process_consultation()

if __name__ == "__main__":
    main()
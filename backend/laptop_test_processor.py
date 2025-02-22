# laptop_test_processor.py
import sounddevice as sd
import numpy as np
import requests
import json
from datetime import datetime
import soundfile as sf
import tempfile
import whisper

class TestAudioProcessor:
    def __init__(self):
        self.api_url = "http://localhost:8000/api/reports"
        print("Loading Whisper model...")
        self.model = whisper.load_model("base")
        print("Test system ready!")
        
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
        """Transcribe audio using Whisper"""
        print("Transcribing audio...")
        result = self.model.transcribe(audio_path)
        
        print("\nTRANSCRIPTION:")
        print("-"*50)
        print(result["text"])
        print("-"*50 + "\n")
        
        return result["text"]

    def simulate_medical_info(self, transcript):
        """Simulate medical entity extraction based on actual transcript"""
        # Simple keyword-based extraction for testing
        medical_entities = {
            "conditions": [],
            "medications": [],
            "symptoms": [],
            "procedures": []
        }
        
        # Basic medical terms to look for
        keywords = {
            "conditions": ["migraine", "diabetes", "hypertension", "asthma"],
            "medications": ["ibuprofen", "aspirin", "paracetamol", "medication"],
            "symptoms": ["headache", "pain", "nausea", "fever", "cough"],
            "procedures": ["surgery", "test", "scan", "x-ray"]
        }
        
        # Look for keywords in transcript
        transcript_lower = transcript.lower()
        for category, terms in keywords.items():
            for term in terms:
                if term in transcript_lower:
                    medical_entities[category].append(term)
        
        print("Extracted Medical Entities:")
        print(json.dumps(medical_entities, indent=2))
        return medical_entities
        
    def send_to_api(self, report_data):
        """Send test report to FastAPI backend"""
        try:
            print("\nSending to API...")
            response = requests.post(
                self.api_url,
                json=report_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            print("Successfully sent to API!")
            print("\nAPI Response:")
            print(json.dumps(response.json(), indent=2))
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending data to API: {e}")
            if hasattr(e, 'response'):
                print("Error details:", e.response.text)
            return None

    def process_test(self):
        """Test processing pipeline"""
        try:
            # Record audio
            audio = self.record_audio()
            
            if audio is not None:
                # Save audio
                audio_path = self.save_audio(audio)
                print(f"Audio saved to: {audio_path}")
                
                # Transcribe audio
                transcript = self.transcribe_audio(audio_path)
                
                # Extract medical entities (simulated but based on actual transcript)
                medical_info = self.simulate_medical_info(transcript)
                
                # Create report
                report = {
                    "timestamp": datetime.now().isoformat(),
                    "transcript": transcript,
                    "medical_entities": medical_info
                }
                
                # Send to API
                result = self.send_to_api(report)
                return result
            
        except Exception as e:
            print(f"Error in test pipeline: {e}")
            return None

def main():
    processor = TestAudioProcessor()
    print("\nStarting test system...")
    print("This version will:")
    print("1. Record your voice until you press Ctrl+C")
    print("2. Transcribe the actual recording")
    print("3. Extract medical entities")
    print("4. Send everything to the API")
    processor.process_test()

if __name__ == "__main__":
    main()
# full_laptop_client.py
import sounddevice as sd
import numpy as np
import requests
from datetime import datetime

class LaptopAudioProcessor:
    def __init__(self):
        self.api_url = "http://localhost:8000/api/reports"
    
    def record_audio(self, duration=5, sample_rate=16000):
        """Record audio from laptop microphone"""
        print(f"Recording for {duration} seconds...")
        audio = sd.rec(int(duration * sample_rate),
                      samplerate=sample_rate,
                      channels=1,
                      dtype='float32')
        sd.wait()
        print("Recording finished!")
        return audio
    
    def simulate_processing(self, audio):
        # For testing, we'll just return a simple processed result
        # In reality, this would use Whisper and spaCy
        return {
            "transcript": "This is a simulated transcript from audio recording",
            "medical_entities": {
                "conditions": ["test condition"],
                "medications": ["test medication"],
                "symptoms": ["test symptom"],
                "procedures": []
            }
        }
    
    def send_to_api(self, report_data):
        try:
            response = requests.post(
                self.api_url,
                json=report_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            print("Success! Response:", response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending data to API: {e}")
            return None

    def process_recording(self):
        # Record audio
        audio = self.record_audio(duration=5)  # 5 seconds for testing
        
        # Process audio (simulated)
        processed_data = self.simulate_processing(audio)
        
        # Create report
        report = {
            "timestamp": datetime.now().isoformat(),
            "transcript": processed_data["transcript"],
            "medical_entities": processed_data["medical_entities"]
        }
        
        # Send to API
        return self.send_to_api(report)

# Run test
if __name__ == "__main__":
    processor = LaptopAudioProcessor()
    processor.process_recording()
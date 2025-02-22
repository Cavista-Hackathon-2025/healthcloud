# test_client.py
import requests
from datetime import datetime

class TestAudioProcessor:
    def __init__(self):
        self.api_url = "http://localhost:8000/api/reports"
    
    def simulate_recording(self):
        return """Patient complains of severe headache and nausea. 
                 Currently taking ibuprofen for pain management. 
                 Previous history of migraines."""
    
    def send_to_api(self, report_data):
        try:
            print("Sending data:", report_data)  # Debug print
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
            if hasattr(e.response, 'text'):
                print("Error details:", e.response.text)
            return None

    def test_connection(self):
        # Match the exact structure expected by Pydantic model
        report = {
            "timestamp": datetime.now().isoformat(),
            "transcript": self.simulate_recording(),
            "medical_entities": {
                "conditions": ["migraine"],
                "medications": ["ibuprofen"],
                "symptoms": ["headache", "nausea"],
                "procedures": []
            }
        }
        
        return self.send_to_api(report)

# Run test
if __name__ == "__main__":
    processor = TestAudioProcessor()
    processor.test_connection()
import sounddevice as sd
import numpy as np
import requests
import json
import whisper
import spacy
from datetime import datetime
import soundfile as sf
import tempfile
from transformers import pipeline

class AudioProcessor:
    def __init__(self):
        print("Loading Whisper model...")
        self.whisper_model = whisper.load_model("base")
        
        print("Loading medical NLP model...")
        try:
            # Use advanced medical spaCy model
            self.nlp = spacy.load("en_core_sci_md")
        except OSError:
            print("Medical spaCy model not found. Please install with:")
            print("pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_core_sci_md-0.4.0.tar.gz")
            raise
        
        # Initialize zero-shot classifier for advanced analysis
        self.classifier = pipeline("zero-shot-classification")
        
        # Medical terminology and analysis components
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
        result = self.whisper_model.transcribe(audio_path)
        print("\nTRANSCRIPTION:")
        print("-"*50)
        print(result["text"])
        print("-"*50 + "\n")
        return result["text"]
        
    def advanced_medical_analysis(self, text):
        """Comprehensive medical analysis using advanced NLP techniques"""
        doc = self.nlp(text)
        
        # Advanced analysis components
        analysis = {
            "symptoms": self._extract_symptoms(text),
            "medical_history": self._extract_medical_history(text),
            "risk_factors": self._identify_risk_factors(text),
            "urgency": self._assess_urgency(text),
            "treatment_suggestions": self._suggest_treatments(text),
            "key_observations": self._extract_key_observations(text)
        }
        
        # Print detailed analysis report
        self._print_comprehensive_report(analysis)
        
        return analysis
    
    def _extract_symptoms(self, text):
        """Extract symptoms using medical NLP"""
        doc = self.nlp(text.lower())
        symptoms = []
        
        # Symptom patterns from medical terminology
        symptom_patterns = [
            "pain", "ache", "discomfort", "swelling", "nausea", 
            "fatigue", "dizziness", "numbness", "weakness"
        ]
        
        for sent in doc.sents:
            for pattern in symptom_patterns:
                if pattern in sent.text.lower():
                    symptoms.append({
                        "symptom": pattern,
                        "context": sent.text.strip(),
                        "severity": self._determine_symptom_severity(sent.text)
                    })
        
        return symptoms
    
    def _determine_symptom_severity(self, text):
        """Determine symptom severity"""
        for level, keywords in self.medical_terms["severity_keywords"].items():
            if any(keyword in text.lower() for keyword in keywords):
                return level
        return "unspecified"
    
    def _extract_medical_history(self, text):
        """Extract medical history mentions"""
        doc = self.nlp(text.lower())
        history = []
        
        history_patterns = [
            "diagnosed with", "history of", "previous", 
            "surgery", "medication", "allergy"
        ]
        
        for sent in doc.sents:
            for pattern in history_patterns:
                if pattern in sent.text:
                    history.append({
                        "description": sent.text.strip(),
                        "category": self._categorize_history_item(sent.text)
                    })
        
        return history
    
    def _categorize_history_item(self, text):
        """Categorize medical history item"""
        categories = {
            "condition": ["diagnosed", "disease", "syndrome"],
            "medication": ["medicine", "drug", "prescription"],
            "procedure": ["surgery", "operation"],
            "allergy": ["allergic", "reaction"]
        }
        
        for category, keywords in categories.items():
            if any(keyword in text.lower() for keyword in keywords):
                return category
        return "other"
    
    def _identify_risk_factors(self, text):
        """Identify potential risk factors"""
        risk_categories = [
            "lifestyle", "family history", "medical history", "environmental"
        ]
        
        # Use zero-shot classification for risk factor identification
        try:
            result = self.classifier(
                text, 
                risk_categories, 
                multi_label=True
            )
            
            return [
                {
                    "category": cat, 
                    "score": score
                } 
                for cat, score in zip(result['labels'], result['scores']) 
                if score > 0.5
            ]
        except Exception as e:
            print(f"Risk factor analysis error: {e}")
            return []
    
    def _assess_urgency(self, text):
        """Assess medical urgency"""
        urgent_indicators = [
            "severe pain", "chest pain", "difficulty breathing", 
            "sudden onset", "severe headache"
        ]
        
        emergency_indicators = [
            "heart attack", "stroke", "cannot breathe", 
            "uncontrolled bleeding"
        ]
        
        # Check for emergency indicators
        for indicator in emergency_indicators:
            if indicator in text.lower():
                return {
                    "level": "emergency",
                    "recommendation": "Immediate emergency care required"
                }
        
        # Check for urgent indicators
        urgent_matches = [
            ind for ind in urgent_indicators 
            if ind in text.lower()
        ]
        
        if urgent_matches:
            return {
                "level": "urgent",
                "indicators": urgent_matches,
                "recommendation": "Prompt medical attention recommended"
            }
        
        return {
            "level": "routine",
            "recommendation": "Standard medical follow-up suggested"
        }
    
    def _suggest_treatments(self, text):
        """Generate treatment suggestions"""
        urgency = self._assess_urgency(text)
        
        # Basic treatment recommendation based on urgency
        treatments = {
            "emergency": [
                "Call emergency services immediately",
                "Seek immediate hospital care",
                "Follow instructions of medical professionals"
            ],
            "urgent": [
                "Schedule urgent medical consultation",
                "Prepare for potential diagnostic tests",
                "Follow recommended immediate care steps"
            ],
            "routine": [
                "Schedule routine check-up",
                "Discuss symptoms with primary care physician",
                "Monitor and track symptoms"
            ]
        }
        
        return treatments.get(urgency['level'], [])
    
    def _extract_key_observations(self, text):
        """Extract key clinical observations"""
        doc = self.nlp(text)
        observations = []
        
        observation_categories = [
            "vital signs", "physical symptoms", 
            "medical conditions", "test results"
        ]
        
        # Use zero-shot classification for observation extraction
        try:
            result = self.classifier(
                text, 
                observation_categories, 
                multi_label=True
            )
            
            return [
                {
                    "category": cat, 
                    "score": score,
                    "context": text
                } 
                for cat, score in zip(result['labels'], result['scores']) 
                if score > 0.5
            ]
        except Exception as e:
            print(f"Observation extraction error: {e}")
            return []
    
    def _print_comprehensive_report(self, analysis):
        """Print a comprehensive medical analysis report"""
        print("\n" + "="*50)
        print("COMPREHENSIVE MEDICAL ANALYSIS REPORT")
        print("="*50)
        
        # Print detailed sections
        print("\nSYMPTOMS:")
        for symptom in analysis.get('symptoms', []):
            print(f"- {symptom['symptom']} (Severity: {symptom.get('severity', 'N/A')})")
        
        print("\nURGENCY ASSESSMENT:")
        urgency = analysis.get('urgency', {})
        print(f"Level: {urgency.get('level', 'Unknown')}")
        print(f"Recommendation: {urgency.get('recommendation', 'N/A')}")
        
        print("\nTREATMENT SUGGESTIONS:")
        for treatment in analysis.get('treatment_suggestions', []):
            print(f"- {treatment}")
        
        print("="*50 + "\n")
    
    def send_to_api(self, data):
        """Send analysis data to API"""
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
            return None

    def process_conversation(self):
        """Main processing pipeline"""
        try:
            audio = self.record_audio()
            
            if audio is not None:
                audio_path = self.save_audio(audio)
                transcript = self.transcribe_audio(audio_path)
                
                # Perform advanced medical analysis
                medical_analysis = self.advanced_medical_analysis(transcript)
                
                # Prepare combined report data
                report_data = {
                    "timestamp": datetime.now().isoformat(),
                    "transcript": transcript,
                    "medical_analysis": medical_analysis
                }
                
                # Send to API (optional)
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
    print("\nStarting advanced medical transcription system...")
    print("Press Ctrl+C to stop recording when finished speaking")
    processor.process_conversation()

if __name__ == "__main__":
    main()
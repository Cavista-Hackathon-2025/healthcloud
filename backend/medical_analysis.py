from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import spacy
from typing import List, Dict, Optional
import re
from datetime import datetime
import numpy as np

class MedicalAnalyzer:
    def __init__(self):
        # Initialize NLP components
        self.classifier = pipeline("zero-shot-classification")
        self.nlp = spacy.load("en_core_sci_md")
        
        # Medical terminology dictionaries
        self.severity_terms = {
            "mild": ["mild", "slight", "minor", "light", "minimal"],
            "moderate": ["moderate", "significant", "noticeable", "considerable"],
            "severe": ["severe", "intense", "extreme", "serious", "grave", "acute"]
        }
        
        self.temporal_terms = {
            "acute": ["sudden", "recent", "just", "acute", "new"],
            "chronic": ["chronic", "long-term", "ongoing", "persistent", "years"]
        }
        
        self.risk_categories = {
            "lifestyle": ["smoking", "alcohol", "diet", "exercise", "stress"],
            "family_history": ["family history", "genetic", "hereditary", "parent", "sibling"],
            "medical_history": ["previous", "history of", "chronic", "diagnosed with"],
            "environmental": ["exposure", "workplace", "environment", "pollution"]
        }

    def extract_symptoms(self, text: str) -> List[Dict]:
        """
        Extract symptoms and their characteristics
        """
        doc = self.nlp(text.lower())
        symptoms = []
        
        # Define symptom patterns
        symptom_patterns = [
            "pain", "ache", "discomfort", "swelling", "nausea", "fatigue",
            "dizziness", "numbness", "tingling", "weakness", "stiffness"
        ]
        
        # Process each sentence
        for sent in doc.sents:
            for pattern in symptom_patterns:
                if pattern in sent.text:
                    # Extract location and characteristics
                    location = self._extract_anatomical_location(sent.text)
                    duration = self._extract_duration(sent.text)
                    severity = self._extract_severity_from_text(sent.text)
                    
                    symptoms.append({
                        "symptom": pattern,
                        "location": location,
                        "duration": duration,
                        "severity": severity,
                        "context": sent.text.strip()
                    })
        
        return symptoms

    def extract_medical_history(self, text: str) -> List[Dict]:
        """
        Extract relevant medical history mentions
        """
        doc = self.nlp(text.lower())
        history = []
        
        # Define history patterns
        history_patterns = {
            "condition": ["diagnosed with", "history of", "suffers from", "had"],
            "surgery": ["surgery", "operation", "procedure"],
            "medication": ["takes", "taking", "prescribed", "medication"],
            "allergy": ["allergic to", "allergy", "reaction"]
        }
        
        for sent in doc.sents:
            for category, patterns in history_patterns.items():
                for pattern in patterns:
                    if pattern in sent.text:
                        history.append({
                            "category": category,
                            "description": sent.text.strip(),
                            "timeframe": self._extract_timeframe(sent.text),
                            "status": self._determine_status(sent.text)
                        })
        
        return history

    def identify_risk_factors(self, text: str) -> List[Dict]:
        """
        Identify potential risk factors from the text
        """
        risk_factors = []
        doc = self.nlp(text.lower())
        
        for category, patterns in self.risk_categories.items():
            for sent in doc.sents:
                for pattern in patterns:
                    if pattern in sent.text:
                        risk_factors.append({
                            "category": category,
                            "factor": self._extract_risk_detail(sent.text, pattern),
                            "context": sent.text.strip(),
                            "severity": self._assess_risk_severity(sent.text)
                        })
        
        return risk_factors

    def suggest_treatments(self, text: str) -> List[Dict]:
        """
        Suggest possible treatments based on analysis
        """
        symptoms = self.extract_symptoms(text)
        severity = self.assess_severity(text)
        
        treatments = []
        for symptom in symptoms:
            treatment = {
                "symptom": symptom["symptom"],
                "recommendations": self._generate_treatment_recommendations(
                    symptom["symptom"],
                    symptom["severity"],
                    severity["level"]
                ),
                "precautions": self._identify_precautions(text),
                "follow_up": self._determine_follow_up_timing(
                    symptom["severity"],
                    severity["level"]
                )
            }
            treatments.append(treatment)
        
        return treatments

    def assess_urgency(self, text: str) -> Dict:
        """
        Assess the urgency level of the case
        """
        # Define urgency indicators
        urgent_indicators = [
            "severe pain", "chest pain", "difficulty breathing",
            "sudden onset", "severe headache", "loss of consciousness"
        ]
        
        emergency_indicators = [
            "unbearable pain", "heart attack", "stroke",
            "severe bleeding", "can't breathe"
        ]
        
        doc = self.nlp(text.lower())
        
        # Check for emergency indicators
        for indicator in emergency_indicators:
            if indicator in text.lower():
                return {
                    "level": "emergency",
                    "confidence": 0.9,
                    "reasoning": [f"Found emergency indicator: {indicator}"],
                    "recommendation": "Immediate emergency care recommended"
                }
        
        # Check for urgent indicators
        urgent_matches = []
        for indicator in urgent_indicators:
            if indicator in text.lower():
                urgent_matches.append(indicator)
        
        if urgent_matches:
            return {
                "level": "urgent",
                "confidence": 0.7,
                "reasoning": [f"Found urgent indicator: {match}" for match in urgent_matches],
                "recommendation": "Prompt medical attention recommended"
            }
        
        # Default to routine
        return {
            "level": "routine",
            "confidence": 0.5,
            "reasoning": ["No urgent or emergency indicators found"],
            "recommendation": "Regular follow-up recommended"
        }

    def extract_key_observations(self, text: str) -> List[Dict]:
        """
        Extract key clinical observations
        """
        doc = self.nlp(text)
        observations = []
        
        # Define observation categories
        categories = {
            "vital_signs": ["temperature", "blood pressure", "pulse", "breathing"],
            "physical_exam": ["swelling", "redness", "tenderness", "reflexes"],
            "patient_state": ["alert", "conscious", "oriented", "distressed"],
            "test_results": ["test", "level", "count", "rate"]
        }
        
        for sent in doc.sents:
            for category, keywords in categories.items():
                for keyword in keywords:
                    if keyword in sent.text.lower():
                        observations.append({
                            "category": category,
                            "observation": sent.text.strip(),
                            "keyword": keyword,
                            "value": self._extract_measurement(sent.text),
                            "timestamp": datetime.now().isoformat()
                        })
        
        return observations

    # Helper methods
    def _extract_anatomical_location(self, text: str) -> str:
        """Extract anatomical location from text"""
        anatomy_terms = ["head", "chest", "back", "arm", "leg", "stomach", "knee", "shoulder"]
        for term in anatomy_terms:
            if term in text.lower():
                return term
        return "unspecified"

    def _extract_duration(self, text: str) -> Dict:
        """Extract duration information from text"""
        duration_patterns = {
            "acute": r"(\d+)\s*(hour|day)s?",
            "chronic": r"(\d+)\s*(week|month|year)s?"
        }
        
        for duration_type, pattern in duration_patterns.items():
            match = re.search(pattern, text.lower())
            if match:
                return {
                    "type": duration_type,
                    "value": match.group(1),
                    "unit": match.group(2)
                }
        return {"type": "unspecified", "value": None, "unit": None}

    def _extract_severity_from_text(self, text: str) -> str:
        """Extract severity level from text"""
        for level, terms in self.severity_terms.items():
            for term in terms:
                if term in text.lower():
                    return level
        return "unspecified"

    def _extract_timeframe(self, text: str) -> Dict:
        """Extract timeframe information"""
        timeframe = {
            "when": "unspecified",
            "duration": "unspecified",
            "ongoing": False
        }
        
        # Add timeframe extraction logic
        if "since" in text.lower():
            timeframe["ongoing"] = True
        
        return timeframe

    def _determine_status(self, text: str) -> str:
        """Determine if condition is active, resolved, or ongoing"""
        if any(word in text.lower() for word in ["current", "ongoing", "still"]):
            return "active"
        elif any(word in text.lower() for word in ["resolved", "past", "previous"]):
            return "resolved"
        return "unknown"

    def _extract_risk_detail(self, text: str, pattern: str) -> str:
        """Extract detailed risk information"""
        # Find the relevant portion of text around the pattern
        pattern_index = text.lower().find(pattern)
        if pattern_index != -1:
            # Extract a window of text around the pattern
            start = max(0, pattern_index - 30)
            end = min(len(text), pattern_index + 50)
            return text[start:end].strip()
        return "unspecified"

    def _assess_risk_severity(self, text: str) -> str:
        """Assess the severity of a risk factor"""
        for level, terms in self.severity_terms.items():
            if any(term in text.lower() for term in terms):
                return level
        return "moderate"

    def _generate_treatment_recommendations(self, symptom: str, 
                                         symptom_severity: str, 
                                         overall_severity: str) -> List[str]:
        """Generate treatment recommendations based on symptoms and severity"""
        recommendations = []
        
        # Basic recommendation logic
        if overall_severity == "severe":
            recommendations.append("Immediate medical evaluation recommended")
        elif overall_severity == "moderate":
            recommendations.append("Schedule follow-up appointment")
            recommendations.append("Monitor symptoms for changes")
        else:
            recommendations.append("Self-monitor and report if symptoms worsen")
        
        return recommendations

    def _identify_precautions(self, text: str) -> List[str]:
        """Identify necessary precautions based on the medical context"""
        precautions = []
        
        # Add precaution identification logic
        if "allergy" in text.lower():
            precautions.append("Check for medication allergies")
        if "diabetes" in text.lower():
            precautions.append("Monitor blood sugar levels")
        
        return precautions

    def _determine_follow_up_timing(self, symptom_severity: str, 
                                  overall_severity: str) -> str:
        """Determine appropriate follow-up timing"""
        if overall_severity == "severe":
            return "immediate"
        elif overall_severity == "moderate":
            return "within 1 week"
        return "as needed"

    def _extract_measurement(self, text: str) -> Optional[str]:
        """Extract measurements and values from text"""
        # Pattern for common medical measurements
        patterns = {
            "temperature": r"(\d+\.?\d*)\s*[°CFcf]",
            "blood_pressure": r"(\d+/\d+)",
            "pulse": r"(\d+)\s*bpm",
            "oxygen": r"(\d+)%"
        }
        
        for measurement, pattern in patterns.items():
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None
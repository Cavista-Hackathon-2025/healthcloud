from core.models import Recording
from core.constants import TRANSCRIPTION_MODEL
from groq import Groq
from django.conf import settings
from typing import Optional

client = Groq(api_key=settings.GROQ_API_KEY)


def transcribe(recording: Recording) -> Optional[str]:
    try:
        with open(recording.file.path, "rb") as file:
            filename = recording.file.name
            transcription = client.audio.transcriptions.create(
                file=(filename, file.read()),
                model=TRANSCRIPTION_MODEL,
                prompt="Specify context or spelling",
                response_format="json",
                language="en",
                temperature=0.0,
            )
            return transcription.text
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None


def extract_report_segments():
    pass

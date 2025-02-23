from pydantic import BaseModel
from datetime import datetime


class ReportSegmentType(BaseModel):
    title: str
    summary: str
    keypoints: list[str]
    priority: int

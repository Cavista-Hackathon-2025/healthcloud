from django.db import models

# Create your models here.


class Recording(models.Model):
    file = models.FileField(upload_to="recordings/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField()
    transcription = models.TextField(blank=True)


class Report(models.Model):
    recording = models.ForeignKey(Recording, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class ReportSegment(models.Model):
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, related_name="segments"
    )
    title = models.CharField(max_length=255)
    summary = models.TextField()
    keypoints = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

from rest_framework import serializers
from core.models import Recording, ReportSegment, Report


class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = [
            "id",
            "file",
            "duration",
            "uploaded_at",
        ]


class UploadRecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = [
            "file",
            "duration",
        ]


class ReportSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportSegment
        fields = [
            "id",
            "report",
            "title",
            "summary",
            "keypoints",
        ]


class ReportSerializer(serializers.ModelSerializer):
    segments = ReportSegmentSerializer(many=True, read_only=True)

    class Meta:
        model = Report
        fields = [
            "id",
            "recording",
            "created_at",
            "segments",
        ]

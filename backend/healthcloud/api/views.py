from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from core.models import Report, Recording
from api.serializers import *

# Create your views here.


class ListReportsView(APIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get(self, request):
        data = ReportSerializer(self.queryset.all(), many=True).data
        return Response(data, status=status.HTTP_200_OK)


class UploadRecordingView(APIView):
    serializer_class = UploadRecordingSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RecordingViewSet(ModelViewSet):
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer

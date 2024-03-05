# labreport/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LabTest, LabReport
from .serializers import LabTestSerializer, LabReportSerializer

class LabTestListCreateAPIView(APIView):
    def get(self, request):
        lab_tests = LabTest.objects.all()
        serializer = LabTestSerializer(lab_tests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LabTestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LabReportListCreateAPIView(APIView):
    def get(self, request):
        lab_reports = LabReport.objects.all()
        serializer = LabReportSerializer(lab_reports, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LabReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

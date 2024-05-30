from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import LabTest
from django.contrib.auth import get_user_model
from .serializers import LabTestSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission

User = get_user_model()

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role.lower() == 'admin'

class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role.lower() == 'receptionist'

class IsLabTech(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role.lower() == 'labtech'
    
class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role.lower() == 'patient'

class LabTestListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsLabTech | IsPatient)

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

class LabTestRetrieveUpdateDeleteView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsLabTech | IsPatient)

    def get(self, request, pk):
        labtest = LabTest.objects.get(id=pk)
        serializer = LabTestSerializer(labtest)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        labtest = LabTest.objects.get(id=pk)
        serializer = LabTestSerializer(labtest, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        labtest = LabTest.objects.get(id=pk)
        serializer = LabTestSerializer(labtest, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        labtest = LabTest.objects.get(id=pk)
        labtest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

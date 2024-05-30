from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Feedback
from .serializers import FeedbackSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.db.models import Q

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

class FeedbackListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated, (IsAdmin | IsReceptionist | IsLabTech | IsPatient))

    def get(self, request):
        search = request.query_params.get('search', None)
        feedbacks = Feedback.objects.all().order_by('-id')
        if search:
            users = users.filter(
                Q(email__icontains=search) |
                Q(feedback_subject__icontains=search)
            )

        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            feedback = Feedback.objects.get(id=pk)
            feedback.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Feedback.DoesNotExist:
            return Response({'error': 'Feedback not found'}, status=status.HTTP_404_NOT_FOUND)

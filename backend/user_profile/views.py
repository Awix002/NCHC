from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer 
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()

class UserExtraDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user_id = request.user.id
            user_profile = UserProfile.objects.get(user_id=user_id)
            user_details = {
                'id': user_profile.id,
                'full_name': request.user.full_name,
                'email': request.user.email,
                'province_state_name': user_profile.province_state_name,
                'city': user_profile.city,
                'address': user_profile.address,
                'date_of_birth': user_profile.date_of_birth,
                'gender': user_profile.gender,
            }
            return Response(user_details, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class UserExtraDetailsUpdate(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        try:
            user_id = request.user.id
            user_profile = UserProfile.objects.get(user_id=user_id)
            user_profile.province_state_name = request.data.get('province_state_name', user_profile.province_state_name)
            user_profile.city = request.data.get('city', user_profile.city)
            user_profile.address = request.data.get('address', user_profile.address)
            user_profile.date_of_birth = request.data.get('date_of_birth', user_profile.date_of_birth)
            user_profile.gender = request.data.get('gender', user_profile.gender)
            user_profile.save()
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

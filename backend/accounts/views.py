from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from .models import UserAccount
from .serializers import UserAccountSerializer 
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.http import JsonResponse
from django.db.models import Q

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

class CheckIsAdmin(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            email = data.get('email')
            if email:
                user = UserAccount.objects.get(email=email)
                is_staff = user.is_staff
                return JsonResponse({'is_staff': is_staff})
            else:
                return JsonResponse({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        except UserAccount.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserAccountListAPIView(APIView):
    permission_classes = (IsAuthenticated, (IsAdmin | IsReceptionist | IsLabTech | IsPatient))

    def get(self, request):
        search = request.query_params.get('search', None)
        users = UserAccount.objects.filter(
            is_active=True,
            is_staff=False,
            role=UserAccount.PATIENT
        )
        
        if search:
            users = users.filter(
                Q(email__icontains=search) |
                Q(full_name__icontains=search) |
                Q(phone_number__icontains=search)
            )
        
        serializer = UserAccountSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAccountRetrieveUpdateDeleteView(APIView):
    permission_classes = (IsAuthenticated, (IsAdmin | IsReceptionist))

    def get_object(self, pk):
        try:
            return UserAccount.objects.get(pk=pk)
        except UserAccount.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_object(pk)
        if user:
            serializer = UserAccountSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        user = self.get_object(pk)
        if user:
            serializer = UserAccountSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        user = self.get_object(pk)
        if user:
            serializer = UserAccountSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class StaffAccountList(APIView):
    permission_classes = (IsAuthenticated, IsAdmin)

    def get(self, request):
        users = UserAccount.objects.filter(
            is_active=True, 
            is_staff=True, 
            role__in=[UserAccount.RECEPTIONIST, UserAccount.LABTECH]
        )
        serializer = UserAccountSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StaffAccountCreate(APIView):
    permission_classes = (IsAuthenticated, IsAdmin)

    def post(self, request):
        try:
            data = request.data
            full_name = data.get('full_name')
            email = data.get('email').lower()
            phone_number = data.get('phone_number')
            password = data.get('password')
            re_password = data.get('re_password')
            role = data.get('role')

            if password == re_password:
                if len(password) >= 8:
                    if not User.objects.filter(email=email).exists():
                        if role in [UserAccount.RECEPTIONIST, UserAccount.LABTECH]:
                            user = User.objects.create_user(full_name=full_name, email=email, phone_number=phone_number, password=password, role=role, is_staff=True, is_active=True)

                            return Response(
                                {'success': f'{role.capitalize()} account created successfully'},
                                status=status.HTTP_201_CREATED
                            )
                        else:
                            return Response(
                                {'error': 'Invalid role specified'},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    else:
                        return Response(
                            {'error': 'User with this email already exists'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                else:
                    return Response(
                        {'error': 'Password must be at least 8 characters in length'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'error': 'Passwords do not match'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {'error': f'Something went wrong when registering an account: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StaffAccountRetrieveUpdateDeleteView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin)

    def get(self, request, pk):
        try:
            account = UserAccount.objects.get(id=pk)
            serializer = UserAccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserAccount.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            account = UserAccount.objects.get(id=pk)
            serializer = UserAccountSerializer(account, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserAccount.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            account = UserAccount.objects.get(id=pk)
            serializer = UserAccountSerializer(account, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserAccount.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            UserAccount.objects.filter(id=pk).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserAccount.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
       
# class UserProfileDetailsAPIView(APIView):
#     permission_classes = (IsAuthenticated, (IsAdmin | IsReceptionist | IsLabTech | IsPatient))

#     def get(self, request):
#         try:
#             user_id = request.user.id  # Get the current user's id
#             user = UserAccount.objects.get(pk=user_id)
#             # Extract user details
#             user_details = {
#                 'id': user.id,
#                 'name': user.full_name,
#                 'email': user.email
#             }
#             return Response(user_details, status=status.HTTP_200_OK)
#         except UserAccount.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# class UserProfileUpdate(APIView):
#     permission_classes = (IsAuthenticated, (IsAdmin | IsReceptionist | IsLabTech | IsPatient))

#     def put(self, request):
#         try:
#             user_data = request.data.get('user')
#             if user_data:
#                 user_id = user_data.get('id')
#                 if user_id:
#                     user = UserAccount.objects.get(pk=user_id)

#                     # Update user details
#                     user.full_name = user_data.get('full_name')
#                     user.email = user_data.get('email')

#                     # Save the updated user
#                     user.save()

#                     # Serialize the updated user and return response
#                     serializer = UserAccountSerializer(user)
#                     return Response(serializer.data, status=status.HTTP_200_OK)
#                 else:
#                     return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response({'error': 'User data is missing'}, status=status.HTTP_400_BAD_REQUEST)
#         except UserAccount.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
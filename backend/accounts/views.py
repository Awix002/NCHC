from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from .models import UserAccount
from .serializers import UserAccountSerializer 

User = get_user_model()

class RegisterStaffView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        try:
            data = request.data
            first_name = data['first_name']
            last_name = data.get('last_name')
            email = data.get('email').lower()
            password = data.get('password')
            re_password = data.get('re_password')
            is_receptionist = data.get('is_receptionist')
            is_labtech = data.get('is_labtech')

            if is_receptionist == 'True':
                is_receptionist = True
            else:
                is_receptionist = False

            if is_labtech == 'True':
                is_labtech = True
            else:
                is_labtech = False
            
            if password == re_password:
                if len(password) >= 8:
                    if not User.objects.filter(email=email).exists():
                        if is_receptionist:
                            User.objects.create_receptionist(first_name=first_name, last_name=last_name, email=email, password=password)

                            return Response(
                                {'success': 'Receptionist account created successfully'},
                                status=status.HTTP_201_CREATED
                            )
                        elif is_labtech:
                            User.objects.create_labtech(first_name=first_name, last_name=last_name, email=email, password=password)

                            return Response(
                                {'success': 'Lab Technician account created successfully'},
                                status=status.HTTP_201_CREATED
                            )
                        
                        else:
                            return Response(
                            {'error': 'Please specify user role as receptionist or lab tech'},
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

class AccountRetrieveUpdateDeleteView(APIView):
    permission_classes = (permissions.AllowAny,) 
    def get(sekf, request, pk):
        account = UserAccount.objects.get(id=pk)
        serializer = UserAccountSerializer(account)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        account = UserAccount.objects.get(id=pk)
        serializer = UserAccountSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        serializer.update(account, validated_data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        account = UserAccount.objects.get(id=pk)
        serializer = UserAccountSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        serializer.update(account, validated_data)

        return Response(serializer.data, status=status.HTTP_200_OK)  

    def delete(self, request, pk):
        UserAccount.objects.filter(id=pk).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    

        #     if password != re_password:
        #         return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        #     if len(password) < 8:
        #         return Response({'error': 'Password must be at least 8 characters in length'}, status=status.HTTP_400_BAD_REQUEST)

        #     email = email.lower()

        #     if User.objects.filter(email=email).exists():
        #         return Response({'error': 'User with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
        #     if is_receptionist:
        #         User.objects.create_receptionist(first_name=first_name, last_name=last_name, email=email, password=password)
        #         return Response({'success': 'Receptionist account created successfully'}, status=status.HTTP_201_CREATED)
            
        #     if is_labtech:
        #         User.objects.create_labtech(first_name=first_name, last_name=last_name, email=email, password=password)
        #         return Response({'success': 'Labtech account created successfully'}, status=status.HTTP_201_CREATED)
            
        # except KeyError:
        #     return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        # except Exception as e:
        #     return Response({'error': f'Something went wrong: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


# class DeleteUserAccountView(APIView): 
#     def delete(self, request, format=None):
#         user = self.request.user

#         try:
#             User.objects.filter(id=user.id).delete()

#             return Response(
#                 {'success': 'Successfully deleted user account'},
#                 status=status.HTTP_200_OK)
#         except:
#             return Response(
#                 {'error': 'Failed to delete user account'},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)

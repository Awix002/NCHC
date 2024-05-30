from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Inventory
from .serializers import InventorySerializer 
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role.lower() == 'admin'

class InventoryListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin)

    def get(self, request):
        category_id = request.query_params.get('category_id')
        search = request.query_params.get('search')
        sort_by_category = request.query_params.get('sort_by_category')

        inventory = Inventory.objects.all()

        # Filter by category if category_id is provided
        if category_id:
            inventory = inventory.filter(category_id=category_id)

        # Search functionality
        if search:
            inventory = inventory.filter(
                Q(name__icontains=search) | Q(vendor__icontains=search) | Q(id__icontains=search)
            )

        # Sorting by category
        if sort_by_category:
            if sort_by_category.lower() == 'asc':
                inventory = inventory.order_by('category__category_name')
            elif sort_by_category.lower() == 'desc':
                inventory = inventory.order_by('-category__category_name')

        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InventorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryRetrieveUpdateDeleteView(APIView):
    permission_classes = (permissions.AllowAny,) 

    def get_object(self, pk):
        try:
            return Inventory.objects.get(pk=pk)
        except Inventory.DoesNotExist:
            return None

    def get(self, request, pk):
        inventory = self.get_object(pk)
        if inventory:
            serializer = InventorySerializer(inventory)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Inventory not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        inventory = self.get_object(pk)
        if inventory:
            serializer = InventorySerializer(inventory, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Inventory not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        inventory = self.get_object(pk)
        if inventory:
            serializer = InventorySerializer(inventory, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Inventory not found'}, status=status.HTTP_404_NOT_FOUND)  

    def delete(self, request, pk):
        inventory = self.get_object(pk)
        if inventory:
            inventory.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Inventory not found'}, status=status.HTTP_404_NOT_FOUND)
        

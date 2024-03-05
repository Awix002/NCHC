from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Inventory
from .serializers import InventorySerializer 


class InventoryListCreateAPIView(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self, request):
        inventory = Inventory.objects.all()

        # # Perform sorting by the default field 'name'
        # inventory = inventory.order_by('name')

        sort_by = request.query_params.get( 'sort_by', 'name')
        # Perform sorting
        inventory = inventory.order_by(sort_by)

        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InventorySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data

        serializer.create(validated_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InventoryRetrieveUpdateDeleteView(APIView):
    permission_classes = (permissions.AllowAny,) 
    def get(sekf, request, pk):
        inventory = Inventory.objects.get(id=pk)
        serializer = InventorySerializer(inventory)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        inventory = Inventory.objects.get(id=pk)
        serializer = InventorySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        serializer.update(inventory, validated_data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        inventory = Inventory.objects.get(id=pk)
        serializer = InventorySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        serializer.update(inventory, validated_data)

        return Response(serializer.data, status=status.HTTP_200_OK)  

    def delete(self, request, pk):
        Inventory.objects.filter(id=pk).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)




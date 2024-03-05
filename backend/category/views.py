# from django.shortcuts import render

# # Create your views here.
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework import permissions
# from .models import Category


# class ListCategoriesView(APIView):
#     permission_classes = (permissions.AllowAny, )

#     def get(self, request, format=None):
#         if Category.objects.all().exists():
#             categories = Category.objects.all()

#             result = []

#             for category in categories:
#                 if not category.parent:
#                     item = {}
#                     item['id'] = category.id
#                     item['name'] = category.name

#                     item['sub_categories'] = []
#                     for cat in categories:
#                         sub_item = {}
#                         if cat.parent and cat.parent.id == category.id:
#                             sub_item['id'] = cat.id
#                             sub_item['name'] = cat.name
#                             sub_item['sub_categories'] = []

#                             item['sub_categories'].append(sub_item)

#                     result.append(item)
#             return Response({'categories': result}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'No categories found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Category


class ListCategoriesView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        # Filter categories without parent categories
        categories = Category.objects.filter(parent=None)

        # Serialize the categories
        serialized_categories = []
        for category in categories:
            serialized_category = {
                'id': category.id,
                'name': category.name
            }
            serialized_categories.append(serialized_category)

        return Response({'categories': serialized_categories}, status=status.HTTP_200_OK)


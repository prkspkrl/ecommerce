from django.shortcuts import render
from .models import Category
from rest_framework.decorators import api_view
# Create your views here.

def category(request):
    return render(request,'category/category.html')




# ----------------------------------------------API------------------------------------------------------------
# ViewSets define the view behavior.
from .serializers import *
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.authentication import BasicAuthentication, TokenAuthentication

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

#To create token
# # users = User.objects.all()
# users = get_user_model().objects.all() # Custom user model to get users list
# for user in users:
# 	token = Token.objects.get_or_create(user=user)
# 	print(token)



class WriteByAdminOnlyPermission(BasePermission):
	def has_permission(self, request, view):
		print(request.user)
		# return True
		user = request.user
		if request.method == 'GET':
			return True

		if request.method == 'POST' or request.method == 'PUT'or request.method == 'DELETE':
			if user.is_superuser:
				return True
		return False

class CategoryList(generics.ListAPIView):
    permission_classes = [IsAuthenticated, WriteByAdminOnlyPermission]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    ordering_fields = ['id','name']
    search_fields = ['category_name','description']


class CategoryViewSet(viewsets.ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated ,WriteByAdminOnlyPermission]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
# class CRUDViewSet(APIView):
# 	def get_object(self,pk):
# 		try:
# 			snippet = Category.objects.get(pk=pk)
# 			return snippet
# 		except:
# 			print('The id does not exists.')
# 	def get(self,request,pk):
# 		snippet = self.get_object(pk)
# 		serializer = CategorySerializer(snippet)
# 		return Response(serializer.data)
#
# 	# @api_view(['POST'])
# 	def post(self,request,pk):
# 		serializer = CategorySerializer(data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# 	def put(self,request,pk):
# 		snippet = self.get_object(pk)
# 		serializer = CategorySerializer(snippet, data=request.data,partial=True)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# 	def delete(self,request,pk):
# 		snippet = self.get_object(pk)
# 		snippet.delete()
# 		return Response(status=status.HTTP_204_NO_CONTENT)
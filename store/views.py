from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

# Create your views here.

def store(request, category_slug=None ):

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories,is_available = True)
        product_count = products.count()

    else:
        products = Product.objects.all().filter(is_available = True)
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,

    }
    return render(request, 'store/store.html',context)


def single_product(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug) #get category's slug,  product table ko category  ko slug
    #category__slug mean 'product ko category' product table bata and tesko slug category ko model bata=> slug by category
    except Exception as e:
        raise e

    context = {
        'single_product' : single_product,
    }

    return render(request,'store/single_product.html',context)


# ----------------------------------------------API------------------------------------------------------------

from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics
from rest_framework import authentication
from .serializers import ProductSerializer
from .models import Product
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token


class WriteByAdminOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        # print('insidnde has permission', request.user)
        user = request.user
        if request.method == 'GET':
            return True
        if request.method == 'POST' or request.method == 'PUT' or request.method == 'DELETE':
            if user.is_superuser:
                return True

        return False


class ProductListView(generics.ListCreateAPIView):
    permission_classes = [WriteByAdminOnlyPermission]
    # IsAuthenticated,
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
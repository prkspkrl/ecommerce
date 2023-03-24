from .models import *
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        # ['url', 'username', 'email', 'is_staff']
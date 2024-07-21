
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class GetuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    
class PendingFriendsRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = '__all__'
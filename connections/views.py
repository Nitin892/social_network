from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from django.db.models import Q
from .serializer import *
from .models import *
from rest_framework.decorators import throttle_classes
from .customerpagination import *
from .customerthrottle import *


class MyCustomThrottle(UserRateThrottle):
    rate = '3/minute'


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request,email = email,password = password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)

            return Response({'msg':'Login successful',"token":token.key})

        
        return Response({'invalid':"credentials"})



class SignUpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')
        first_name = request.data.get('first_name')

        if not email:
            return Response({'error': 'Email is required'})
        if not password:
            return Response({'error': 'Password is required'})
        if not username:
            return Response({'error': 'Username is required'})

        
        if User.objects.filter(email = email).exists():
            return Response({'message':"email is already taken"})

        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username is already taken'})
        
        newuser = User(email = email,password = make_password(password),username=username)
        newuser.save()

        return Response({"success":"User created"})

        
class GetuserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        query = request.data.get('query')
        results = User.objects.filter(Q(email=query) | Q(username__icontains=query)).order_by('-username')
    
        paginator = SetPagination()
        paginated_results = paginator.paginate_queryset(results, request)
        serialized_data = GetuserSerializer(paginated_results,many=True)

        return paginator.get_paginated_response(serialized_data.data)


class SendInvitationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [MyCustomThrottle]

    def post(self,request):
        id = request.data.get('id')
        sender = request.user
        receiver = User.objects.get(id = id)

        if request.user.id == id:
            return Response({'error':"You can't invite yourself"})

        if Invitation.objects.filter(from_user = request.user,to_user =receiver).exists():
            return Response({'error':'Invitation already send'})
        

        Invitation_obj = Invitation(
            from_user = sender,
            to_user = receiver,
        )
        Invitation_obj.save()

        return Response({'msg':'Invitation send successfully'})


class RespondFriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        id = request.data.get('id')
        action = request.data.get('action')

        invitation_obj = Invitation.objects.get(from_user = request.user,to_user = id)
        invitation_obj.invitation_type = action
        if action == 'accept':
            invitation_obj.invitation_type
            invitation_obj.save()
            return Response({"success": "Friend request accepted"})
        elif action == 'reject':
            invitation_obj.invitation_type = 'rejected'
            invitation_obj.save()
            return Response({"success": "Friend request rejected"})


class PendingFriendsRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        results = Invitation.objects.filter(from_user = request.user,invitation_type = 'send')
        serialized_data = PendingFriendsRequestSerializer(results,many=True)
        return Response(serialized_data.data)



class AcceptedFriendsRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        results = Invitation.objects.filter(from_user = request.user,invitation_type = 'accept')
        serialized_data = PendingFriendsRequestSerializer(results,many=True)
        return Response(serialized_data.data)




class RejectedFriendsRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        results = Invitation.objects.filter(from_user = request.user,invitation_type = 'reject')
        serialized_data = PendingFriendsRequestSerializer(results,many=True)
        return Response(serialized_data.data)





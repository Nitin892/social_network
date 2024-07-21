from django.urls import path
from . views import *


urlpatterns = [
    path('login',LoginAPIView.as_view()),
    path('signup',SignUpAPIView.as_view()),
    path('get-user',GetuserAPIView.as_view()),
    path('invite-friend',SendInvitationAPIView.as_view()),
    path('respond-friends-request',RespondFriendRequestAPIView.as_view()),
    path('pending-friends-request',PendingFriendsRequestAPIView.as_view()),
    path('accepted-friends-request',AcceptedFriendsRequestAPIView.as_view()),
    path('rejected-friend-request', RejectedFriendsRequestAPIView.as_view())

]
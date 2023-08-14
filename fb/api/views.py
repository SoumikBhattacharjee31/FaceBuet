from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connections

from .models import Users, Settings, ReplyReact, PostSharedInPage, PostSharedByUser, PostReact, PostMedia
from .models import PostInPage, PostDesc, PostComment, Post, PageOwned, PageMedia, PageLike, Page
from .models import MessageMedia, Message, Media, MarketplaceOwning, MarketplaceMedia, Marketplace
from .models import FriendReq, Events, EventMedia, EventHosting, EventInterested
from .serializers import UsersSerializer, SettingsSerializer, ReplyReactSerializer, PostSharedInPageSerializer, PostSharedByUserSerializer, PostReactSerializer, PostMediaSerializer
from .serializers import PostInPageSerializer, PostDescSerializer, PostCommentSerializer, PostSerializer, PageOwnedSerializer, PageMediaSerializer, PageLikeSerializer, PageSerializer
from .serializers import MessageMediaSerializer, MessageSerializer, MediaSerializer, MarketplaceOwningSerializer, MarketplaceMediaSerializer, MarketplaceSerializer
from .serializers import FriendReqSerializer, EventsSerializer, EventMediaSerializer, EventHostingSerializer, EventInterestedSerializer

# Create your views here.
@api_view(['GET'])
def getUsers(request):
    users=Users.objects.all()
    serializer = UsersSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def setUsers(request):
    print("hello")
    user_name = request.data.get('user_name')
    password = request.data.get('password')
    mobile = request.data.get('mobile')
    profile_pic = request.data.get('profile_pic')
    cover_photo = request.data.get('cover_photo')
    birth_date = request.data.get('birth_date')
    Users.objects.create(user_name=user_name, password=password, mobile_number=mobile,profile_pic=profile_pic, cover_photo=cover_photo,birth_date=birth_date)
    with connections['default'].cursor() as cursor:
        cursor.execute("INSERT INTO USERS VALUES (2, %s, %s, %s, %s, %s, TO_DATE(%s, 'YYYY-MM-DD'))",
            [user_name, password, mobile,profile_pic,cover_photo, birth_date])
            
        
             


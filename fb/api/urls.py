from django.urls import path
from . import views

urlpatterns = [
    path('addusers/', views.setUsers, name='addusers'),
    path('signIn/', views.signIn, name='signIn'),
    path('home/', views.homePage, name='home'),
    path('set_user_post/', views.set_user_post, name='set_user_post'),
    path('get_groups/', views.get_groups, name='groups'),
    path('get_friend_list/', views.get_friend_list, name='get_friend_list'),
    path('get_friend_req_list/', views.get_friend_req_list, name='get_friend_req_list'),
    path('get_friend_req_list/', views.get_friend_req_list, name='get_friend_req_list'),
    path('get_chat_friend_list/', views.get_chat_friend_list, name='get_chat_friend_list'),
    # path('get_user_profile/', views.get_user_profile, name='get_user_profile'),
]

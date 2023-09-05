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
    path('get_events/', views.get_events, name='get_events'),
    path('set_event/', views.set_event, name='set_event'),
    path('search_users/', views.search_users, name='search_users'),
    path('get_marketplace/', views.get_marketplace, name='get_marketplace'),
    path('set_marketplace/', views.set_marketplace, name='set_marketplace'),
    path('get_user_profile/', views.get_user_profile, name='get_user_profile'),
    path('get_comment_info/', views.get_comment_info, name='get_comment_info'),
]

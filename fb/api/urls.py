from django.urls import path
from . import views

urlpatterns = [
    # path('users/',views.getUsers,name="users"),
    path('addusers/', views.setUsers, name='addusers'),
    path('signIn/', views.signIn, name='signIn'),
    path('home/', views.homePage, name='home'),
    path('set_user_post/', views.set_user_post, name='home'),
    # path('addImages/', views.setImages, name='addImages'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('users/',views.getUsers,name="users"),
    path('addusers/', views.setUsers, name='addusers'),
    path('signIn/', views.signIn, name='signIn'),
    path('addImages/', views.setImages, name='addImages'),
]
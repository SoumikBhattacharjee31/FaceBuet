from django.urls import path
from . import views

urlpatterns = [
    path('users/',views.getUsers,name="users"),
   path('addusers/', views.setUsers, name='addusers'),


]
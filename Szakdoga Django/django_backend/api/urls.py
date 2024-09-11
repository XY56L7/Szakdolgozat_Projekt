from django.urls import path
from .views import get_users, create_user, user_detail, get_energy_data

urlpatterns = [
    path('users/',get_users,name='get_users'),
    path('users/create/', create_user ,name='create_user'),
    path('users/<int:pk>', user_detail ,name='user_detail'),
    path('users/energy/', get_energy_data ,name='get_energy_data')

]

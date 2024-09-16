from django.urls import path
from .views import get_energy_data, evaluate_model ,register, login,get_users

urlpatterns = [
    # path('users/',get_users,name='get_users'),
    # path('users/create/', create_user ,name='create_user'),
    # path('users/<int:pk>', user_detail ,name='user_detail'),
    path('users/energy/', get_energy_data ,name='get_energy_data'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('users/', get_users, name='get_users'),
    path('predict/', evaluate_model, name='predict_and_plot')
]

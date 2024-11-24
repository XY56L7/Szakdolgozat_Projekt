from django.conf import settings
from django.urls import path
from .views import get_energy_data, evaluate_model ,register, login,get_users
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/energy/', get_energy_data ,name='get_energy_data'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('users/', get_users, name='get_users'),
    path('predict/', evaluate_model, name='predict_and_plot'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



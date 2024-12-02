from django.conf import settings
from django.urls import path
from .views import  evaluate_model, predict_energy ,register, login
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('predict_energy/', predict_energy, name='predict_energy'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('predict/', evaluate_model, name='predict_and_plot'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

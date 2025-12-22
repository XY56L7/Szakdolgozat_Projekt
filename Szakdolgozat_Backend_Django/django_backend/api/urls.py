from django.conf import settings
from django.urls import path
from .views import  evaluate_model, predict_energy, register, login, predict_communities, predict_communities_gru
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('predict_energy/', predict_energy, name='predict_energy'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('predict/', evaluate_model, name='predict_and_plot'),
    path('predict_communities/', predict_communities, name='predict_communities_and_plot'),
    path('predict_communities_gru/', predict_communities_gru, name='predict_gru')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.urls import path
from .views import get_energy_data, evaluate_model ,register, login,get_users
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('users/energy/', get_energy_data ,name='get_energy_data'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('users/', get_users, name='get_users'),
    path('predict/', evaluate_model, name='predict_and_plot')
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from django.conf import settings
# from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Write debug information to a file
    with open("debug_info.txt", "w") as debug_file:
        debug_file.write(f"MEDIA_URL: {settings.MEDIA_URL}\n")
        debug_file.write(f"MEDIA_ROOT: {settings.MEDIA_ROOT}\n")
        
        # Write each URL pattern's path to the file
        debug_file.write("URL Patterns:\n")
        for pattern in urlpatterns:
            debug_file.write(f"{pattern.pattern}\n")  # Write the pattern as a string




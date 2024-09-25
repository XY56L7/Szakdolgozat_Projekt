import os
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import EnergyAnalysisSerializer, RegisterSerializer, UserSerializer
from django.contrib.auth.models import User

# your_app/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import numpy as np
import pandas as pd
import json
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import joblib
import matplotlib.pyplot as plt
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import random
import matplotlib
from asgiref.sync import sync_to_async
import time
matplotlib.use('Agg')

# IMAGE_DIR = r'C:\Users\Martin\Desktop\szakdoga\Projekt\Szakdolgozat_Projekt\Szakdoga Angular\szakdolgozat-frontend\src\assets\images'
# IMAGE_DIR_2 = r'C:\Users\Martin\Desktop\szakdoga\Projekt\Szakdolgozat_Projekt\Szakdoga Angular\szakdolgozat-frontend\dist\angular-tour-of-heroes\browser\assets\images'
# model = load_model(r'C:\Users\Martin\Desktop\szakdoga\Projekt\Szakdolgozat_Projekt\Szakdoga Django\django_backend\api\models\washing_machine.keras')
# scaler = joblib.load(r'C:\Users\Martin\Desktop\szakdoga\Projekt\Szakdolgozat_Projekt\Szakdoga Django\django_backend\api\models\washing_machine_scaler.pkl')

BASE_DIR = settings.BASE_DIR 
MEDIA_DIR = os.path.join(BASE_DIR, 'api', 'media')
MODEL_PATH = os.path.join(BASE_DIR, 'api', 'models', 'washing_machine.keras')
SCALER_PATH = os.path.join(BASE_DIR, 'api', 'models', 'washing_machine_scaler.pkl')

model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
# Define your prediction function
def predict_power_consumption(v_rms, i_rms, s, p):

    #model = load_model(r'C:\Users\Martin\Desktop\szakdoga\Projekt\Szakdolgozat_Projekt\Szakdoga Django\django_backend\api\models\washing_machine.keras')

    input_data = np.array([[v_rms, i_rms, s, p]])
    input_data_scaled = scaler.transform(input_data)
    input_data_scaled = np.reshape(input_data_scaled, (1, 1, 4))  # 1 time step, 4 features
    
    prediction = model.predict(input_data_scaled)
    predicted_power = float(prediction[0, 3])

    return predicted_power



@csrf_exempt
@require_http_methods(["POST"])
async def evaluate_model(request):
    try:
        data = json.loads(request.body)

        v_rms = float(data.get('V_rms'))
        i_rms = float(data.get('I_rms'))
        s = float(data.get('S'))
        p = float(data.get('P'))

        predicted_power = await sync_to_async(predict_power_consumption)(v_rms, i_rms, s, p)

        fig, ax = plt.subplots()
        ax.plot([v_rms, i_rms, s, p], label='Input Data')
        ax.set_title('Predicted Power Consumption')
        ax.set_xlabel('Features')
        ax.set_ylabel('Value')
        ax.legend()

        random_number = random.randint(0, 10000)
        image_filename = f'prediction_plot{random_number}.png'
        image_path = os.path.join(MEDIA_DIR, image_filename)

        image_path = os.path.normpath(image_path)  
        print(f"image_path: {image_path}")

        plt.savefig(image_path)
        plt.close(fig) 
        if os.path.exists(image_path):
            print(image_path)
            print("A kép létezik.")
        else:
            print("A kép nem létezik.")

        response_data = {
            'image_path': request.build_absolute_uri('/api' + settings.MEDIA_URL + image_filename),  
            'predicted_power': predicted_power
        }

        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# Ensure that predict_power_consumption is defined as a regular function
def predict_power_consumption(v_rms, i_rms, s, p):
    # Prepare the input data
    input_data = np.array([[v_rms, i_rms, s, p]])
    input_data_scaled = scaler.transform(input_data)
    input_data_scaled = np.reshape(input_data_scaled, (1, 1, 4))  # 1 time step, 4 features
    
    # Make prediction
    prediction = model.predict(input_data_scaled)
    predicted_power = float(prediction[0, 3])

    return predicted_power
# @csrf_exempt
# @require_http_methods(["POST"])
# def evaluate_model(request):
#     try:
#         # Get variables from request
#         data = json.loads(request.body)

#         v_rms = float(data.get('V_rms'))
#         i_rms = float(data.get('I_rms'))
#         s = float(data.get('S'))
#         p = float(data.get('P'))

#         # Predict power consumption
#         predicted_power = predict_power_consumption(v_rms, i_rms, s, p)

#         # Create a plot
#         fig, ax = plt.subplots()
#         ax.plot([v_rms, i_rms, s, p], label='Input Data')
#         ax.set_title('Predicted Power Consumption')
#         ax.set_xlabel('Features')
#         ax.set_ylabel('Value')
#         ax.legend()

#         # Define the path to save the image
#         random_number = random.randint(0, 10000)
#         image_filename = f'prediction_plot4918.png'
#         image_path = os.path.join(MEDIA_DIR, image_filename)
#         print(f"Saving file at: {image_path}")

#         # Save the plot as a PNG file
#         # plt.savefig(image_path)
#         # plt.close(fig)  # Close the plot to free memory
#         time.sleep(1)

#         # Return the image path and prediction as JSON
#         response_data = {
#             'image_path': request.build_absolute_uri(settings.MEDIA_URL + image_filename),  # Send the full image path in the response
#             'predicted_power': predicted_power
#         }
#         return JsonResponse(response_data)

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()  # Get all users
    serializer = UserSerializer(users, many=True)  # Serialize the data
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def register(request):
    print("Line 9 Register method in views.py")
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    from django.contrib.auth import authenticate
    from rest_framework_simplejwt.tokens import RefreshToken

    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'userName': username
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def get_energy_data(request):
        # Fake data
        fake_data = {
            "device_option": "option1",
            "devices": ["device1", "device2", "device3"],
            "time_interval": "1h",
            "prediction_model": "basic_model",
            "V_rms": 220.5,
            "I_rms": 10.2,
            "P": 2235.1,
            "S": 2300.0,
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "custom_model_file": None  # No file uploaded
        }

        # Serialize the fake data
        serializer = EnergyAnalysisSerializer(fake_data)

        # Return the serialized data as JSON
        return Response(serializer.data, status=status.HTTP_200_OK)
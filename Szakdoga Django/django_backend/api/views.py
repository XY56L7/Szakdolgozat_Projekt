import os
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
import io
import base64
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import random


IMAGE_DIR = r'C:\Users\Martin\Desktop\szakdoga\Projekt\Szakdolgozat_Projekt\Szakdoga Angular\szakdolgozat-frontend\src\assets\images'
model = load_model(r'C:\Users\Martin\Desktop\szakdoga\Projekt\Szakdolgozat_Projekt\Szakdoga Django\django_backend\api\models\washing_machine.keras')
scaler = joblib.load(r'C:\Users\Martin\Desktop\szakdoga\Projekt\Szakdolgozat_Projekt\Szakdoga Django\django_backend\api\models\washing_machine_scaler.pkl')
# Define your prediction function
def predict_power_consumption(v_rms, i_rms, s, p):

    # Load the model
    model = load_model(r'C:\Users\Martin\Desktop\szakdoga\Projekt\Szakdolgozat_Projekt\Szakdoga Django\django_backend\api\models\washing_machine.keras')

    # Initialize scaler
# Prepare the input data
    input_data = np.array([[v_rms, i_rms, s, p]])
    input_data_scaled = scaler.transform(input_data)
    input_data_scaled = np.reshape(input_data_scaled, (1, 1, 4))  # 1 time step, 4 features
    
    # Make prediction
    prediction = model.predict(input_data_scaled)
    predicted_power = float(prediction[0, 3])

    return predicted_power
# Define your view function
import logging
logger = logging.getLogger(__name__)
@csrf_exempt
@require_http_methods(["POST"])
def evaluate_model(request):
    try:
        # Get variables from request
        data = json.loads(request.body)

        v_rms = float(data.get('V_rms'))
        i_rms = float(data.get('I_rms'))
        s = float(data.get('S'))
        p = float(data.get('P'))

        # Predict power consumption
        predicted_power = predict_power_consumption(v_rms, i_rms, s, p)

        # Create a plot
        fig, ax = plt.subplots()
        ax.plot([v_rms, i_rms, s, p], label='Input Data')
        ax.set_title('Predicted Power Consumption')
        ax.set_xlabel('Features')
        ax.set_ylabel('Value')
        ax.legend()

# Define the path to save the image
        random_number = random.randint(0,10000)
        image_filename = f'prediction_plot{random_number}.png'
        image_path = os.path.join(IMAGE_DIR, image_filename)

        # Save the plot as a PNG file
        plt.savefig(image_path)
        plt.close(fig)  # Close the plot to free memory

        import time

        time.sleep(5)  # Delay execution by 2 seconds

        # Return the image path and prediction as JSON
        response_data = {
            'image_path': random_number,
            'predicted_power': predicted_power
        }
        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
# @csrf_exempt
# @require_http_methods(["POST"])
# def evaluate_model(request):
#     try:
#         # Get variables from request
#         data = json.loads(request.body)
        
#         logger.info(f"Received data: {data}")

#         v_rms = float(data.get('V_rms'))
#         i_rms = float(data.get('I_rms'))
#         s = float(data.get('S'))
#         p = float(data.get('P'))

#         # Predict power consumption
#         predicted_power = predict_power_consumption(v_rms, i_rms, s, p)

#         # Return prediction as JSON
#         response_data = {
#             'predicted_power': predicted_power
#         }

#         print(response_data)
#         return JsonResponse(response_data)

#     except Exception as e:
#         logger.error(f"Error: {str(e)}")
#         return JsonResponse({'error': str(e)}, status=400)



# @csrf_exempt
# @require_http_methods(["POST"])
# def predict_and_plot(request):
#     data = json.loads(request.body)
    
#     v_rms = data.get('V_rms')
#     i_rms = data.get('I_rms')
#     s = data.get('S')
#     p = data.get('P')
    
#     # Bemeneti adatok előkészítése

#     model = load_model('api\models\washing_machine.keras')
#     scaler = MinMaxScaler(feature_range=(0, 1))

#     input_data = np.array([[v_rms, i_rms, s, p]])
#     input_data_scaled = scaler.transform(input_data)
#     input_data_scaled = np.reshape(input_data_scaled, (1, 1, 4))
    
#     # Előrejelzés
#     prediction = model.predict(input_data_scaled)
#     predicted_p = prediction[0, 3]
    
#     # Grafikon generálása
#     import matplotlib.pyplot as plt
#     from io import BytesIO
#     import base64

#     # Készítünk egy példaként grafikont
#     plt.figure(figsize=(10, 5))
#     plt.plot([v_rms, i_rms, s, p], label='Input Features')
#     plt.title('Example Plot')
#     plt.xlabel('Features')
#     plt.ylabel('Values')
#     plt.legend()
    
#     # Mentjük a grafikont egy bufferbe
#     buf = BytesIO()
#     plt.savefig(buf, format='png')
#     buf.seek(0)
#     image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    
#     response_data = {
#         'predicted_P': predicted_p,
#         'plot': image_base64
#     }
    
#     return JsonResponse(response_data)

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
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# @api_view(['GET'])
# def get_users(request):
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def create_user(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET','PUT','DELETE'])
# def user_detail(request,pk):
#     try:
#         user = User.objects.get(pk = pk)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = UserSerializer(user,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#Sample for testing the communication with the frontend
#Actually it is working

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
import os
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import EnergyAnalysisSerializer, RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
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
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import random
import matplotlib
from asgiref.sync import sync_to_async
matplotlib.use('Agg')


def encode_season(season):
    seasons = ["Winter", "Spring", "Summer", "Autumn"]
    return [1 if s == season else 0 for s in seasons]

def encode_category(category):
    categories = ["kertes ház", "ikerház", "panel"]
    return [1 if c == category else 0 for c in categories]

@csrf_exempt
def predict_energy(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            year = data.get('year')
            month = data.get('month')
            day = data.get('day')
            hour = data.get('hour')
            number_of_panels = data.get('number_of_panels')
            season = data.get('season')  
            category = data.get('category') 

            season_encoded = encode_season(season)
            category_encoded = encode_category(category)

            features = [
                year, month, day, hour, number_of_panels, *season_encoded, *category_encoded
            ]

            print(features)

            production = predict_production(features)
            consumption = predict_consumption(features)

            return JsonResponse({'production_power': production, 'consumption_power': consumption})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


# Termelés predikció
def predict_production(features):
    model_path = os.path.join(settings.BASE_DIR, 'api', 'models', 'production_model.keras')
    scaler_path = os.path.join(settings.BASE_DIR, 'api', 'models', 'scaler.pkl')
    model = load_model(model_path)
    scaler = joblib.load(scaler_path)

    # Skálázás és predikció
    features_scaled = scaler.transform([features])

    prediction = model.predict(features_scaled)
    return float(prediction[0][0])

def predict_consumption(features):
    model_path = os.path.join(settings.BASE_DIR, 'api', 'models', 'consumption_model.keras')
    scaler_path = os.path.join(settings.BASE_DIR, 'api', 'models', 'scaler.pkl')
    model = load_model(model_path)
    scaler = joblib.load(scaler_path)

    features_scaled = scaler.transform([features])
    
    prediction = model.predict(features_scaled)
    return float(prediction[0][0])


BASE_DIR = settings.BASE_DIR 
MEDIA_DIR = os.path.join(BASE_DIR, 'api', 'media')

def predict_power_consumption(v_rms, i_rms, s,device):
    MODEL_PATH = os.path.join(BASE_DIR, 'api', 'models', f'{device}',f'{device}.keras')

    INPUT_SCALER = os.path.join(BASE_DIR, 'api', 'models', f'{device}',f'{device}_scaler_features.pkl')
    OUTPUT_SCALER = os.path.join(BASE_DIR, 'api', 'models', f'{device}',f'{device}_scaler_target.pkl')
    model = load_model(MODEL_PATH)

    input_scaler = joblib.load(INPUT_SCALER)
    output_scaler = joblib.load(OUTPUT_SCALER)

    input_data = pd.DataFrame([[v_rms, i_rms, s]], columns=['V_rms', 'I_rms', 'S'])
    
    input_data_scaled = input_scaler.transform(input_data)
    input_data_scaled = np.reshape(input_data_scaled, (1, 1, 3))

    prediction = model.predict(input_data_scaled)

    print(f'Prediction: {prediction}')
    
    predicted_power_scaled = prediction[0, 0]  

    predicted_power = output_scaler.inverse_transform([[predicted_power_scaled]])[0][0]

    return abs(predicted_power)



@csrf_exempt
@require_http_methods(["POST"])
async def evaluate_model(request):
    try:
        print("Raw request body:", request.body)
        
        data = json.loads(request.body)
        print("Parsed data:", data)
        
        if 'V_rms' not in data or 'I_rms' not in data or 'S' not in data:
            return JsonResponse({'error': 'Missing required input fields'}, status=400)

        v_rms = float(data.get('V_rms'))
        i_rms = float(data.get('I_rms'))
        s = float(data.get('S'))
        device = str(data.get('Device'))
        print(f"Extracted values - V_rms: {v_rms}, I_rms: {i_rms}, S: {s}")

        predicted_power = await sync_to_async(predict_power_consumption)(v_rms, i_rms, s,device)
        print("Predicted power:", predicted_power)

        fig, ax = plt.subplots()
        ax.plot([v_rms, i_rms, s], label='Input Data')
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
            print("Image exists:", image_path)
        else:
            print("Image does not exist.")

        response_data = {
            'image_path': request.build_absolute_uri('/api' + settings.MEDIA_URL + image_filename),
            'predicted_power': predicted_power
        }

        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except ValueError as e:
        return JsonResponse({'error': f'Invalid input data: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@api_view(['GET'])
def get_users(request):
    users = User.objects.all()  # Get all users
    serializer = UserSerializer(users, many=True) 
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
            "custom_model_file": None  
        }

        serializer = EnergyAnalysisSerializer(fake_data)

        return Response(serializer.data, status=status.HTTP_200_OK)
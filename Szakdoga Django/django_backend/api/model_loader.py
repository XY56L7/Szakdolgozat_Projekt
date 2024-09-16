# # your_app/model_loader.py
# from keras.models import load_model
# import numpy as np
# import pandas as pd
# from sklearn.preprocessing import MinMaxScaler

# # Betöltjük a modellt
# def load_trained_model():
#     return load_model('api\models\washing_machine.keras')

# # Skálázó betöltése
# def load_scaler(training_data):
#     scaler = MinMaxScaler(feature_range=(0, 1))
#     # Skálázó beállítása (az adattal való tanulás itt szükséges)
#     return scaler

# model = load_trained_model()
# scaler = load_scaler()

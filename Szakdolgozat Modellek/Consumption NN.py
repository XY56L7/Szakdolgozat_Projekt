# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, GRU, Bidirectional, Embedding
from keras.optimizers import SGD
import math
from sklearn.metrics import mean_squared_error
import tensorflow as tf
from tensorflow.keras import layers, models

# Some functions to help out with
def plot_predictions(test,predicted):
    plt.plot(test, color='red',label='Real Values')
    plt.plot(predicted, color='blue',label='Predicted Values')
    plt.title('Prediction')
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.legend()
    plt.show()

def return_rmse(test,predicted):
    rmse = math.sqrt(mean_squared_error(test, predicted))
    print("The root mean squared error is {}.".format(rmse))

# First, we get the data
# First, we get the data
df = pd.read_csv('/content/drive/MyDrive/data.csv', parse_dates=True)
#df.index_freq='15min'
df['Date'] = pd.to_datetime(df['Date'],format = '%Y-%m-%d %H:%M:%S')
db = df[df['Device'] == 'Washing_Machine']
dataset = db[['Date','V_rms', 'V_rms50' ,'I_rms', 'P','S']]
dataset = dataset.dropna()
dataset = dataset.set_index('Date')

# Selecting V_rms, I_rms, S as features and P as the target variable
features = ['V_rms', 'I_rms', 'S']  # Features
target = 'P'  # Target variable

# Splitting the dataset into training and test sets
training_set = dataset[:'2022-02-22'][features].values  # Features for training
training_target = dataset[:'2022-02-22'][target].values.reshape(-1, 1)  # Target for training

test_set = dataset['2022-02-22':][features].values  # Features for testing
test_target = dataset['2022-02-22':][target].values.reshape(-1, 1)  # Target for testing

# Scaling the features and target
sc_features = MinMaxScaler(feature_range=(0, 1))
sc_target = MinMaxScaler(feature_range=(0, 1))

training_set_scaled = sc_features.fit_transform(training_set)
training_target_scaled = sc_target.fit_transform(training_target)

# Preparing the data structure with 60 timesteps and multiple features (V_rms, I_rms, S)
X_train = []
y_train = []
for i in range(60, len(training_set_scaled)):
    X_train.append(training_set_scaled[i-60:i])  # Appending features for each timestep
    y_train.append(training_target_scaled[i, 0])  # Appending target (P)

X_train, y_train = np.array(X_train), np.array(y_train)

# Reshaping X_train for efficient modeling (samples, timesteps, features)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], len(features)))

# The GRU architecture (kept the same as your original)
regressorGRU = Sequential()
# First GRU layer with Dropout regularisation
regressorGRU.add(GRU(units=100, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2]), activation='tanh'))
regressorGRU.add(Dropout(0.1))
# Second GRU layer
regressorGRU.add(GRU(units=100, return_sequences=True, activation='tanh'))
regressorGRU.add(Dropout(0.1))
# Third GRU layer
regressorGRU.add(GRU(units=100, return_sequences=True, activation='tanh'))
regressorGRU.add(Dropout(0.1))
# Fourth GRU layer
regressorGRU.add(GRU(units=50, activation='tanh'))
regressorGRU.add(Dropout(0.1))
# Dense layers
regressorGRU.add(Dense(units=64, activation='relu'))
regressorGRU.add(Dense(units=32, activation='relu'))
# Output layer for regression
regressorGRU.add(Dense(units=1))

# Compiling the RNN
regressorGRU.compile(optimizer='RMSprop', loss='mse')

# Fitting the model to the training set
regressorGRU.fit(X_train, y_train, epochs=10, batch_size=32)

# Preparing the test set for prediction
test_set_scaled = sc_features.transform(test_set)
X_test = []
for i in range(60, len(test_set_scaled)):
    X_test.append(test_set_scaled[i-60:i])

X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], len(features)))

# Predicting using the GRU model
GRU_predicted = regressorGRU.predict(X_test)
GRU_predicted = sc_target.inverse_transform(GRU_predicted)

# Visualizing the results
plot_predictions(test_target, GRU_predicted)

# Evaluating the model with RMSE
return_rmse(test_target, GRU_predicted)


# Given input values
input_values = np.array([[0.5, 1, 2]])  # V_rms, I_rms, S

# Scaling the input values using the same scaler as for training (sc_features)
input_scaled = sc_features.transform(input_values)

# Since the GRU model expects a 3D input (samples, timesteps, features), we need to reshape the input
# Assuming the model was trained with 60 timesteps, we need to provide 60 previous timesteps
# As we only have 1 data point, we will duplicate the input to fill 60 timesteps
input_reshaped = np.repeat(input_scaled, 60, axis=0).reshape(1, 60, len(features))

# Make the prediction
predicted_P_scaled = regressorGRU.predict(input_reshaped)

# Inverse transform to get the original scale of P
predicted_P = sc_target.inverse_transform(predicted_P_scaled)

# Output the predicted value of P
print("Predicted P value:", predicted_P[0][0])


# Save the scalers using pickle
with open('scaler_features_printer.pkl', 'wb') as f:
    pickle.dump(sc_features, f)

with open('scaler_target_printer.pkl', 'wb') as f:
    pickle.dump(sc_target, f)

import pickle

# Get the model's weights
model_weights = regressorGRU.get_weights()

# Save the weights using pickle
with open('gru_model_weights_printer.pkl', 'wb') as f:
    pickle.dump(model_weights, f)

# A model mentése natív Keras formátumban
regressorGRU.save('gru_model_printer.keras')
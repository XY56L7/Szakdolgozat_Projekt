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


df = pd.read_csv('/content/drive/MyDrive/Projekt/data.csv', parse_dates=True)
df['Date'] = pd.to_datetime(df['Date'],format = '%Y-%m-%d %H:%M:%S')
db = df[df['Device'] == 'Washing_Machine']
dataset = db[['Date','V_rms', 'V_rms50' ,'I_rms', 'P','S']]
dataset = dataset.dropna()
dataset = dataset.set_index('Date')

training_set = dataset[:'2022-02-22'].iloc[:,3:4].values
test_set = dataset['2022-02-22':].iloc[:,3:4].values


sc = MinMaxScaler(feature_range=(0,1))
training_set_scaled = sc.fit_transform(training_set)


X_train = []
y_train = []
for i in range(60,len(training_set)):
    X_train.append(training_set_scaled[i-60:i,0])
    y_train.append(training_set_scaled[i,0])
X_train, y_train = np.array(X_train), np.array(y_train)

X_train = np.reshape(X_train, (X_train.shape[0],X_train.shape[1],1))

regressorGRU = Sequential()
regressorGRU.add(GRU(units=100, return_sequences=True, input_shape=(X_train.shape[1],1), activation='tanh'))
regressorGRU.add(Dropout(0.1))
regressorGRU.add(GRU(units=100, return_sequences=True, input_shape=(X_train.shape[1],1), activation='tanh'))
regressorGRU.add(Dropout(0.1))
regressorGRU.add(GRU(units=100, return_sequences=True, input_shape=(X_train.shape[1],1), activation='tanh'))
regressorGRU.add(Dropout(0.1))
regressorGRU.add(GRU(units=50, activation='tanh'))
regressorGRU.add(Dropout(0.1))
regressorGRU.add(Dense(units=64, activation='relu'))
regressorGRU.add(Dense(units=32, activation='relu'))
regressorGRU.add(Dense(units=1))


learning_rate = 0.01
momentum = 0.9
nesterov = True
optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate, momentum=momentum, nesterov=nesterov)
regressorGRU.compile(optimizer='RMSprop', loss='mse')
regressorGRU.fit(X_train,y_train,epochs=10,batch_size=32)


dataset_total = pd.concat((dataset["P"][:'2022-02-20'],dataset["P"]['2022-02-20':]),axis=0)
inputs = dataset_total[len(dataset_total)-len(test_set) - 60:].values
inputs = inputs.reshape(-1,1)
inputs  = sc.fit_transform(inputs)

X_test = []
for i in range(60,len(inputs)):
    X_test.append(inputs[i-60:i,0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
GRU_predicted_stock_price = regressorGRU.predict(X_test)
GRU_predicted_stock_price = sc.inverse_transform(GRU_predicted_stock_price)

plot_predictions(test_set,GRU_predicted_stock_price)

return_rmse(test_set,GRU_predicted_stock_price)
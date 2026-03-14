import keras
from keras import layers
from tensorflow import keras as tf_keras

model = keras.Sequential([
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])
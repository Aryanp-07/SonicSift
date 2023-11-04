# importing libraries
import warnings

warnings.filterwarnings("ignore")
import numpy as np
import librosa
import os
import keras
import librosa.display

# sample testing for shape of the audio file
songname = f"/gtzan-dataset-music-genre-classification/Data/genres_original/blues/blues.00000.wav"
y, sr = librosa.load(songname, mono=True, duration=2, offset=0)
ps = librosa.feature.melspectrogram(y=y, sr=sr, hop_length=256, n_fft=512, n_mels=128)
ps = librosa.power_to_db(ps**2)
print(ps.shape)

# creating a dataset with preprocessed audio files
dataset = []
genres = {
    "blues": 0,
    "classical": 1,
    "country": 2,
    "disco": 3,
    "hiphop": 4,
    "jazz": 5,
    "metal": 6,
    "pop": 7,
    "reggae": 8,
    "rock": 9,
}

for genre, genre_number in genres.items():
    for filename in os.listdir(
        f"/gtzan-dataset-music-genre-classification/Data/genres_original/{genre}"
    ):
        songname = f"/gtzan-dataset-music-genre-classification/Data/genres_original/{genre}/{filename}"
        try:
            for index in range(14):
                y, sr = librosa.load(songname, mono=True, duration=2, offset=index * 2)
                ps = librosa.feature.melspectrogram(
                    y=y, sr=sr, hop_length=256, n_fft=512, n_mels=64
                )
                ps = librosa.power_to_db(ps**2)
                dataset.append((ps, genre_number))
        except Exception as e:
            print(f"{e}")
print(len(dataset))


import random

random.shuffle(dataset)

train = dataset[:10000]
valid = dataset[10000:12000]
test = dataset[12000:]

X_train, Y_train = zip(*train)
X_valid, Y_valid = zip(*valid)
X_test, Y_test = zip(*test)


# Reshape for CNN input
X_train = np.array([x.reshape((64, 173, 1)) for x in X_train])
X_valid = np.array([x.reshape((64, 173, 1)) for x in X_valid])
X_test = np.array([x.reshape((64, 173, 1)) for x in X_test])

# One-Hot encoding for classes
Y_train = np.array(keras.utils.to_categorical(Y_train, 10))
Y_valid = np.array(keras.utils.to_categorical(Y_valid, 10))
Y_test = np.array(keras.utils.to_categorical(Y_test, 10))


# Classification with Keras
import keras
from keras import Input
from keras.layers import LSTM
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten, GRU

len(X_train)
X_train.shape
n_features = X_train.shape[2]
input_shape = (None, X_train.shape[1])
print(input_shape)
model_input = Input(input_shape, name="input")
print(model_input)
print(X_train.shape)


# Building CNN-LSTM Model
from keras.layers import Reshape

model = Sequential()

model.add(
    Conv2D(
        20,
        (5, 5),
        input_shape=(64, 173, 1),
        activation="relu",
        strides=1,
        padding="valid",
    )
)
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(50, (5, 5), use_bias=50))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(20, activation="relu"))
model.add(Reshape((20, 1)))
model.add(LSTM(512, activation="relu", return_sequences=False))
model.add(Dense(10, activation="softmax"))
model.summary()

# Compiling the model with optimizer
from keras.optimizers import Adam

model.compile(
    optimizer=Adam(lr=1e-5), loss="categorical_crossentropy", metrics=["accuracy"]
)

# plotting the model
from tensorflow.keras.utils import plot_model

plot_model(model)


# Training the model
from keras.callbacks import EarlyStopping

early_stopping = EarlyStopping(monitor="val_loss", patience=50, verbose=2)
history = model.fit(
    X_train,
    Y_train,
    epochs=200,
    batch_size=64,
    validation_data=(X_test, Y_test),
    callbacks=[early_stopping],
)

model.save("sonicsift.keras")
model.save("sonicsift.h5")
model.save_weights("my_model_weights.hdf5")

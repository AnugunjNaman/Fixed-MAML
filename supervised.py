# -*- coding: utf-8 -*-
"""Ml_miniproject

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JLyDC0EWkTIKGxrUTZwFO1UGxX9Ygu0F

#-
"""

from google.colab import drive
drive.mount("/content/gdrive")

!pip install speechpy>=2.2
!pip install h5py>=2.7.1

# Commented out IPython magic to ensure Python compatibility.
import os
import sys
import numpy as np
import scipy.io.wavfile as wav
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
from speechpy.feature import mfcc

import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from matplotlib.pyplot import specgram
import pandas as pd
import glob 
from sklearn.metrics import confusion_matrix
import IPython.display as ipd  # To play sound in the notebook
import warnings

os.getcwd()

path = '/content/gdrive/My Drive/data'

os.chdir(path)

os.getcwd()

ls

emotions = {'ans':'fear', 'dis':'disgust', 'gio':'happy', 'rab':'anger', 'tri':'sad'}
language = {'en': 'english', 'es':'spanish', 'it':'italian'}
gender   = {'f':'female', 'm':'male'}

fname = '/content/gdrive/My Drive/data/Anger/f_rab064aen.wav'

data, sampling_rate = librosa.load(fname)
plt.figure(figsize=(15, 5))
librosa.display.waveplot(data, sr=sampling_rate)

ipd.Audio(fname)

whale_song, _ = librosa.effects.trim(data)
plt.figure(figsize=(15, 5))

librosa.display.waveplot(whale_song, sr=sampling_rate);

fname = '/content/gdrive/My Drive/data/Anger/m_rab121ben.wav'

data, sampling_rate = librosa.load(fname)
plt.figure(figsize=(15, 5))
librosa.display.waveplot(data, sr=sampling_rate)

ipd.Audio(fname)

fname = '/content/gdrive/My Drive/data/Happy/m_gio145aen.wav'

data, sampling_rate = librosa.load(fname)
plt.figure(figsize=(15, 5))
librosa.display.waveplot(data, sr=sampling_rate)

ipd.Audio(fname)

import librosa                    
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def mel_spec(path):
  file_location = path
  wave, sr = librosa.load(file_location)
  plt.figure(figsize=(15, 5))
  librosa.display.waveplot(wave, sr=sr)
  melSpec = librosa.feature.melspectrogram(y=wave, sr=sr, n_mels=40, hop_length=160, n_fft=480, fmin=20, fmax=4000)
  melSpec_dB = librosa.power_to_db(melSpec, ref=np.max)
  plt.figure(figsize=(10, 5))
  librosa.display.specshow(melSpec_dB, x_axis='time', y_axis='mel', sr=sr, fmax=4000)
  plt.colorbar(format='%+1.0f dB')
  plt.title("MelSpectrogram")
  plt.tight_layout()
  plt.show()

def convert_mfcc(folder_path):
  df = pd.DataFrame(columns=['path', 'feature', 'language', 'gender', 'emotion'])
  # counter = 0
  folder = ['/Anger', '/Sad', '/Happy', '/Disgust', '/Fear']

  data_path = []
  data_feature = []
  data_language = []
  data_gender = []
  data_emotion = []
  counter = 0
  for emotion in folder:
    print(emotion)
    path = folder_path + emotion
    allfiles = os.listdir(path)
    allfiles = [path + '/' + filename for filename in allfiles]
    # count = 0
    for index, file_path in enumerate(allfiles):
      try:
        X, sample_rate = librosa.load(file_path, res_type='kaiser_fast', duration=2.5 ,sr=16000, offset=0.5)

        sample_rate = np.array(sample_rate)
        # mean as the feature. Could do min and max etc as well. 
        
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40), axis=0)
        print(index, file_path)
        # print(mfccs)
        # data_feature.append(mfccs)
        df.loc[counter, 'feature'] = list(mfccs)
        counter += 1
        data_language.append(language[file_path.split('/')[-1][9:11]])
        data_gender.append(gender[file_path.split('/')[-1][0]])
        data_emotion.append(emotions[file_path.split('/')[-1][2:5]])
        data_path.append(file_path)
        # count += 1
      except:
        continue
      # if count == 150:
        # break

  # print(len(df['feature']))
  df['path'] = data_path
  # df['feature'] = data_feature
  df['language'] = data_language
  df['gender'] = data_gender
  df['emotion'] = data_emotion

  return df

dataset = convert_mfcc('/content/gdrive/My Drive/data')

dataset.head()

dataset['feature'].loc[0]

dataset.to_csv('/content/gdrive/My Drive/data/SER.csv', index=False)

"""#--"""

ser_df = pd.read_csv('/content/gdrive/My Drive/data/SER.csv', converters={'feature': eval})

ser_df

ser_df['language'].value_counts()

import keras
from keras import regularizers
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, Model, model_from_json
from keras.layers import Dense, Embedding, LSTM
from keras.layers import Input, Flatten, Dropout, Activation, BatchNormalization
from keras.layers import Conv1D, MaxPooling1D, AveragePooling1D
from keras.utils import np_utils, to_categorical
from keras.callbacks import ModelCheckpoint

# sklearn
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Other  
import librosa
import librosa.display
import json
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from matplotlib.pyplot import specgram
import pandas as pd
import seaborn as sns
import glob 
import os
import pickle
import IPython.display as ipd

def n_shot(n, df, test_df):
  a_df = df[df['emotion'] == 'anger'].sample(n = n)
  s_df = df[df['emotion'] == 'sad'].sample(n = n)
  h_df = df[df['emotion'] == 'happy'].sample(n = n)
  f_df = df[df['emotion'] == 'fear'].sample(n = n)
  d_df = df[df['emotion'] == 'disgust'].sample(n = n)


  train = pd.concat([a_df, s_df, h_df, f_df, d_df])
  test = test_df.sample(n = 25)
  return train, test

def language_specific_model(lang, n):
  ser_df['feature'] = ser_df['feature'].apply(lambda x: np.array(x))

  lang_ser = ser_df[ser_df['language'] == lang]
  non_lang_ser = ser_df[ser_df['language'] != lang]

  lang_df = pd.concat([lang_ser['emotion'].reset_index()['emotion'], pd.DataFrame(lang_ser['feature'].values.tolist())], axis=1)

  non_lang_df = pd.concat([non_lang_ser['emotion'].reset_index()['emotion'], pd.DataFrame(non_lang_ser['feature'].values.tolist())], axis=1)

  lang_df=lang_df.fillna(0)
  non_lang_df=non_lang_df.fillna(0)

  train, test = n_shot(20,df=non_lang_df, test_df=lang_df)

  x_train, y_train = train.drop(['emotion'], axis=1), train['emotion']
  x_test, y_test = test.drop(['emotion'], axis=1), test['emotion']

  x_train = np.array(x_train)
  y_train = np.array(y_train)
  x_test = np.array(x_test)
  y_test = np.array(y_test)

  lb = LabelEncoder()
  y_train = np_utils.to_categorical(lb.fit_transform(y_train))
  y_test = np_utils.to_categorical(lb.fit_transform(y_test))


  x_train = np.expand_dims(x_train, axis=2)
  x_test = np.expand_dims(x_test, axis=2)


  model = Sequential()
  model.add(Conv1D(256, 8, padding='same',input_shape=(x_train.shape[1],1)))  # X_train.shape[1] = No. of Columns
  model.add(Activation('relu'))
  model.add(Conv1D(256, 8, padding='same'))
  model.add(BatchNormalization())
  model.add(Activation('relu'))
  model.add(Dropout(0.25))
  model.add(MaxPooling1D(pool_size=(8)))
  model.add(Conv1D(128, 8, padding='same'))
  model.add(Activation('relu'))
  model.add(Conv1D(128, 8, padding='same'))
  model.add(Activation('relu'))
  model.add(Conv1D(128, 8, padding='same'))
  model.add(Activation('relu'))
  model.add(Conv1D(128, 8, padding='same'))
  model.add(BatchNormalization())
  model.add(Activation('relu'))
  model.add(Dropout(0.25))
  model.add(MaxPooling1D(pool_size=(8)))
  model.add(Conv1D(64, 8, padding='same'))
  model.add(Activation('relu'))
  model.add(Conv1D(64, 8, padding='same'))
  model.add(Activation('relu'))
  model.add(Flatten())
  model.add(Dense(5)) # Target class number
  model.add(Activation('softmax'))

  model.summary()


  opt = optimizers.RMSprop(lr=0.00001, decay=1e-6)

  model.compile(loss='categorical_crossentropy', optimizer=opt,metrics=['accuracy'])
  model_history = model.fit(x_train, y_train, epochs=100, validation_data=(x_test, y_test))

  plt.plot(model_history.history['loss'])
  plt.plot(model_history.history['val_loss'])
  plt.title('model loss')
  plt.ylabel('loss')
  plt.xlabel('epoch')
  plt.legend(['train', 'test'], loc='upper left')
  plt.title(f"{n}-shot learning")
  plt.show()

"""## english in testset, and other languages in trainset"""

language_specific_model('english', n=5)

language_specific_model('english', n=10)

language_specific_model('english', n=20)

"""## spanish in testset, and other languages in trainset"""

language_specific_model('spanish', n=5)

language_specific_model('spanish', n=10)

language_specific_model('spanish', n=20)

"""## italian in testset, and other languages in trainset"""

language_specific_model('italian', n=5)

language_specific_model('italian', n=10)

language_specific_model('italian', n=20)


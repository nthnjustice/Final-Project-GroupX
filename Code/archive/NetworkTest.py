import math
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, Activation, SpatialDropout2D, MaxPooling2D, Flatten, Dense
from keras.layers import AveragePooling2D, Dropout, BatchNormalization, GlobalAveragePooling2D
from keras.optimizers import SGD, Adam
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
from sklearn.metrics import confusion_matrix, classification_report


path_train = '/home/ubuntu/Final-Project-Group1/Code/data/train'
path_validation = '/home/ubuntu/Final-Project-Group1/Code/data/validation'
path_test = '/home/ubuntu/Final-Project-Group1/Code/data/test'
path_output = '/home/ubuntu/Final-Project-Group1/Code/nj/'

img_width = 100
img_height = 100
target_size = (img_width, img_height)

epochs = 200
batch_size = 32

# generator = ImageDataGenerator(horizontal_flip=True, vertical_flip=True)
# train_generator = generator.flow_from_directory(
#     path_train,
#     target_size=target_size,
#     batch_size=batch_size,
#     color_mode='grayscale',
#     class_mode='categorical'
# )
#
# generator = ImageDataGenerator()
# validation_generator = generator.flow_from_directory(
#     path_validation,
#     target_size=target_size,
#     batch_size=batch_size,
#     color_mode='grayscale',
#     class_mode='categorical'
# )
#
# generator = ImageDataGenerator()
# test_generator = generator.flow_from_directory(
#     path_test,
#     target_size=target_size,
#     batch_size=batch_size,
#     color_mode='grayscale',
#     class_mode='categorical',
#     shuffle=False,
#     seed=42
# )



model = Sequential([
    Convolution2D(32, kernel_size=(10, 10), input_shape=(img_width, img_height, 1)),
    BatchNormalization(),
    Activation('relu'),
    MaxPooling2D(pool_size=(5, 5)),
    SpatialDropout2D(0.2),

    Convolution2D(64, kernel_size=(5, 5)),
    BatchNormalization(),
    Activation('relu'),
    MaxPooling2D(pool_size=(2, 2)),
    SpatialDropout2D(0.2),

    Convolution2D(128, kernel_size=(3, 3)),
    BatchNormalization(),
    Activation('relu'),
    AveragePooling2D(pool_size=(5, 5)),
    SpatialDropout2D(0.2),

    Flatten(),
    Dense(700),
    Activation('relu'),
    Dropout(0.5),
    Dense(9),
    Activation('softmax')
])
model.summary()
# model.compile(optimizer=Adam(lr=0.0001), loss='categorical_crossentropy', metrics=['acc'])
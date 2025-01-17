# code for Nathan's custom CNN implementation (re-used for every model iteration, see GitHub logs for previous versions)

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


def nj():
    print('running nj model')
    path_train = 'data/train'
    path_validation = 'data/validation'
    path_test = 'data/test'
    path_output = 'outputs/nj/'

    img_width = 100
    img_height = 100
    target_size = (img_width, img_height)

    epochs = 1000
    batch_size = 32

    generator = ImageDataGenerator(horizontal_flip=True, vertical_flip=True)
    train_generator = generator.flow_from_directory(
        path_train,
        target_size=target_size,
        batch_size=batch_size,
        color_mode='grayscale',
        class_mode='categorical'
    )

    generator = ImageDataGenerator()
    validation_generator = generator.flow_from_directory(
        path_validation,
        target_size=target_size,
        batch_size=batch_size,
        color_mode='grayscale',
        class_mode='categorical'
    )

    generator = ImageDataGenerator()
    test_generator = generator.flow_from_directory(
        path_test,
        target_size=target_size,
        batch_size=batch_size,
        color_mode='grayscale',
        class_mode='categorical',
        shuffle=False,
        seed=42
    )

    model = Sequential([
        Convolution2D(32, kernel_size=(5, 5), strides=(1, 1), input_shape=(img_width, img_height, 1)),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(3, 3), padding='same',),
        SpatialDropout2D(0.2),

        Convolution2D(64, kernel_size=(5, 5), strides=(1, 1)),
        BatchNormalization(),
        Activation('relu'),
        MaxPooling2D(pool_size=(3, 3), padding='same',),
        SpatialDropout2D(0.2),

        Convolution2D(128, kernel_size=(5, 5), strides=(1, 1)),
        BatchNormalization(),
        Activation('relu'),
        SpatialDropout2D(0.2),
        GlobalAveragePooling2D(),

        Dense(700),
        Activation('relu'),
        Dropout(0.5),
        Dense(9),
        Activation('softmax')

        ###

        # Convolution2D(32, kernel_size=(5, 5), padding='same', input_shape=(img_width, img_height, 1)),
        # Activation('relu'),
        # MaxPooling2D(pool_size=(3, 3), padding='same'),
        # Convolution2D(65, kernel_size=(5, 5), padding='same'),
        # Activation('relu'),
        # GlobalAveragePooling2D(),
        # Dense(32),
        # Activation('relu'),
        # Dropout(0),
        # Dense(2),
        # Activation('softmax')
    ])

    model.compile(optimizer=SGD(lr=0.01, decay=1e-6, momentum=0.9), loss='categorical_crossentropy', metrics=['acc'])

    history = model.fit_generator(
        train_generator,
        epochs=epochs,
        validation_data=validation_generator,
        callbacks=[ModelCheckpoint(path_output + 'nj_model.hdf5', monitor="val_loss")]
    )

    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig(path_output + 'nj_acc.png')
    plt.show()

    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig(path_output + 'nj_loss.png')
    plt.show()

    model = load_model(path_output + 'nj_model.hdf5')
    steps = test_generator.n // test_generator.batch_size
    test_generator.reset()
    loss, acc = model.evaluate_generator(test_generator, steps=steps, verbose=0)
    print("loss: ", loss)
    print("acc: ", acc)

    y_pred = model.predict_generator(test_generator, steps + 1)
    y_pred = np.argmax(y_pred, axis=1)
    print('Confusion Matrix')
    print(confusion_matrix(test_generator.classes, y_pred))
    print('Classification Report')
    print(classification_report(test_generator.classes, y_pred))

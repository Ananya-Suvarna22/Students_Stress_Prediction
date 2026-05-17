from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Flatten, Dense

def build_cnn():

    model = Sequential()

    model.add(
        Conv2D(
            32,
            (3,3),
            activation='relu',
            input_shape=(48,48,1)
        )
    )

    model.add(
        MaxPooling2D(2,2)
    )

    model.add(
        Conv2D(
            64,
            (3,3),
            activation='relu'
        )
    )

    model.add(
        MaxPooling2D(2,2)
    )

    model.add(Flatten())

    model.add(
        Dense(
            128,
            activation='relu'
        )
    )

    model.add(
        Dense(
            3,
            activation='softmax'
        )
    )

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model
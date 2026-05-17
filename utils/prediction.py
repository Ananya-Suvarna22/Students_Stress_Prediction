import numpy as np
from keras.models import load_model

model = load_model("stress_model.h5")

emotion_labels = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Neutral",
    "Sad",
    "Surprise"
]

def predict_stress(face):

    face = face / 255.0
    face = np.reshape(face, (1,48,48,1))

    prediction = model.predict(face)

    return np.argmax(prediction)